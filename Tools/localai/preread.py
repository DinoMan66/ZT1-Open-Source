#!/usr/bin/env python3
"""
preread.py - let the local model pre-read the next functions before a session starts. Free tool (Tools\\TOOLS.md).

    py Tools\\localai\\preread.py                  the 15 cheapest targets of Tools\\next.py of 64 bytes or more
    py Tools\\localai\\preread.py --top 25 --folder gx      (any next.py filter: --folder, --max-size)
    py Tools\\localai\\preread.py --collect        merge the digests that have arrived into PREREAD.md
    py Tools\\localai\\preread.py --va 0x4e9989 0x4e9a10        digests of these functions (JPOG: Dll:0xrva) -> out\\pre_<id>.md
    py Tools\\localai\\preread.py --evidence 0x61f8c0 ...       NAMING EVIDENCE for placeholder-named functions: every
                       caller's use of it, its strings and callees, at most two name candidates with the lines
                       that support them -> out\\ev_<id>.md (for documentation rounds)
A Claude session can ask for any of these without the user: Tools\\queue\\preread_<id>.txt holding the options on
one line (for example `--evidence 0x61f8c0 0x4d3de0`); watch_ai.py runs it and answers the questions it queues.
start_local_ai.bat runs the first form automatically, so starting the local model is enough.

For every target it queues one question for watch_ai.py (Tools\\queue\\ask_pre_<target>.json) with the Ghidra C of
the function, of the functions it calls (up to 4) and the call sites in up to 2 callers, and asks for a short
digest: what the function does, which fields and parameters it reads and writes, what the callees seem to do,
the strings it uses. The digests arrive in Tools\\localai\\out\\pre_<target>.md; Tools\\localai\\out\\PREREAD.md lists
the targets in order with their digests (refresh it with --collect).

A digest is a HINT from a small model about Ghidra's output, which is itself a guess: it saves reading, it is not
evidence. Names, types and layouts still come from the binary and the rules (CLAUDE.md "Local model").
"""
import argparse, glob, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
QUEUE = os.path.join(ROOT, "Tools", "queue")
OUT = os.path.join(HERE, "out")
PLAN = os.path.join(OUT, "PREREAD.md")
LIST = os.path.join(OUT, "next.json")
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
MARK = re.compile(r"^// ==== ([0-9a-fA-F]{8})  (.+?)  \(size (\d+) bytes\)")
MAX_LINES = 220                       # per included function: enough for the shape, not a whole giant caller

QUESTION = ("This is Ghidra's decompilation of one function (the TARGET, first) and of functions it calls or that "
            "call it. Write a digest of the TARGET for someone who will rewrite it in C++: 1) what it does, in two "
            "or three sentences; 2) the fields it reads and writes, as offset -> read/write -> what it seems to "
            "hold, for `this` / param_1 and any other pointer parameter; 3) each call it makes and what the callee "
            "seems to do (one line each); 4) every string or constant that hints at a name, quoted exactly; 5) loops, "
            "switches and early returns. Say 'unknown' instead of guessing names.")


EVIDENCE_Q = ("This is Ghidra's decompilation of one function (the TARGET, first), the functions it calls, and the "
              "places that call it. Collect EVIDENCE for the TARGET's real name; do not invent: 1) what it does in one "
              "sentence; 2) every string it or its callers use near the call, quoted exactly with its line; 3) what each "
              "caller does with it (passes what, uses the result how), one line per caller with the line number; 4) at "
              "most two name candidates, each followed by the exact lines that support it, or 'no evidence' if nothing "
              "in the text points to a name. A candidate without a supporting line is not allowed.")


def c_files():
    if ZOO:
        return [os.path.join(ROOT, "decompiled", "zoo.exe.c")]
    return sorted(glob.glob(os.path.join(ROOT, "decompiled", "*.c")))


def index(path):
    """-> {address: (first line, last line, name)} and {name: address} of one Ghidra export (cached by mtime)"""
    cache = os.path.join(ROOT, ".cache", "preread_" + os.path.basename(path) + ".json")
    stamp = f"{os.path.getsize(path)}-{int(os.path.getmtime(path))}"
    try:
        c = json.load(open(cache, encoding="utf-8"))
        if c["stamp"] == stamp:
            return {int(k): tuple(v) for k, v in c["by_va"].items()}
    except Exception:
        pass
    by_va, cur = {}, None
    with open(path, encoding="latin1") as f:
        for n, ln in enumerate(f, 1):
            m = MARK.match(ln)
            if m:
                if cur: by_va[cur[0]] = (cur[1], n - 1, cur[2])
                cur = (int(m.group(1), 16), n, m.group(2))
        if cur: by_va[cur[0]] = (cur[1], n, cur[2])
    try:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        json.dump({"stamp": stamp, "by_va": {str(k): v for k, v in by_va.items()}}, open(cache, "w", encoding="utf-8"))
    except OSError:
        pass
    return by_va


def image_base(dll):
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True):
        b = os.path.splitext(os.path.basename(p).replace("_inst", ""))[0]
        if b.lower() == dll.lower() and p.lower().endswith((".dll", ".exe")):
            import struct
            d = open(p, "rb").read(4096)
            pe = struct.unpack_from("<I", d, 0x3c)[0]
            return struct.unpack_from("<I", d, pe + 0x34)[0]
    return 0x10000000


def c_file_for(dll):
    for p in c_files():
        b = os.path.basename(p).replace("_inst", "").split(".")[0]
        if b.lower() == dll.lower():
            return p


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def spec_for(path, first, last, limit=MAX_LINES):
    return f"{rel(path)}:{first}-{min(last, first + limit - 1)}"


def build_question(t, evidence=False):
    """-> the ask json for one next.py entry, or None when Ghidra has no such function"""
    ncallers, ctx = (8, 20) if evidence else (2, 12)
    if ZOO:
        path, va = c_files()[0], t["va"]
    else:
        path = c_file_for(t["dll"]); va = image_base(t["dll"]) + t["va"]
    if not path or not os.path.exists(path):
        return None
    by_va = index(path)
    ident = ("ev_" if evidence else "pre_") + re.sub(r"[^\w.-]+", "_", t["key"])[:50]
    question = EVIDENCE_Q if evidence else QUESTION
    if va not in by_va:
        dis = disassembly(t, ident)                  # not in Ghidra's export: give the model the machine code
        if not dis:
            return None
        return {"id": ident, "question": f"TARGET: {t.get('name') or 'the function'} at {t['key']} (x86 machine code, Ghidra has no C for it). "
                + question, "files": [dis], "max_words": 260}
    first, last, gname = by_va[va]
    by_name = {}
    for k, v in by_va.items():
        parts = v[2].split("::")
        for i in range(len(parts)):
            by_name.setdefault("::".join(parts[i:]), k)          # Ghidra writes TFile::~TFile for Toshi::TFile::~TFile
    lines = open(path, encoding="latin1").read().split("\n")
    body = "\n".join(lines[first - 1:last])
    files = [spec_for(path, first, last, 600)]
    # callees: FUN_xxxxxxxx (Zoo / unnamed) or Ghidra's names (JPOG exports)
    callees = []
    for m in re.finditer(r"((?:[A-Za-z_]\w*::)*~?[A-Za-z_]\w*)\s*\(", body):
        nm = m.group(1)
        addr = int(nm[4:], 16) if re.match(r"^FUN_[0-9a-fA-F]{8}$", nm) else by_name.get(nm)
        if addr and addr != va and addr in by_va and addr not in callees:
            callees.append(addr)
    for c in callees[:4]:
        f, l, _ = by_va[c]; files.append(spec_for(path, f, l, 80))
    # callers: the lines around a call of the target in up to 2 other functions
    short = gname.split("::")[-1]
    pat = re.compile(r"\b" + re.escape(gname if gname.startswith("FUN_") else short) + r"\s*\(")
    starts = sorted((v[0], v[1], k) for k, v in by_va.items())
    found, owners = 0, set()
    for n, ln in enumerate(lines, 1):
        if first <= n <= last or not pat.search(ln) or ln.startswith("//"):
            continue
        owner = next((s for s in reversed(starts) if s[0] <= n), None)
        if owner and owner[2] != va and owner[2] not in owners:
            owners.add(owner[2])
            files.append(f"{rel(path)}:{max(owner[0], n - ctx - 3)}-{min(owner[1], n + ctx)}")
            found += 1
            if found == ncallers: break
    if evidence and not found:
        question += " (No direct caller was found: it is probably called through a vtable or a function pointer.)"
    return {"id": ident, "question": f"TARGET: {gname} ({t.get('name') or gname}). " + question, "files": files,
            "max_words": 320 if evidence else 260}


def make_target(tok):
    """'0x4e9989' (Zoo) / 'TKernelInterface:0x141c0' (JPOG) -> a target entry like next.py's"""
    if ZOO:
        va = int(tok, 16)
        return {"key": f"{va:#x}", "va": va, "size": None, "name": ""}
    if ":" not in tok:
        raise SystemExit(f"{tok}: JPOG targets are <Dll>:<rva>, e.g. TKernelInterface:0x141c0")
    dll, r = tok.split(":", 1); rva = int(r, 16)
    return {"key": f"{dll} {rva:#x}", "va": rva, "dll": dll, "size": 400, "name": ""}


def disassembly(t, ident):
    """write the target's disassembly to Tools/localai/out/<ident>.dis.txt (for functions Ghidra did not export)"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("next_tool", os.path.join(ROOT, "Tools", "next.py"))
        N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
        NB = N.load("neighbours_tool", os.path.join(ROOT, "Tools", "neighbours.py"))
        if ZOO:
            img = NB.F.Image(os.path.join(ROOT, "Original", "zoo.exe")); va, size = t["va"], None
        else:
            p = next((p for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True)
                      if os.path.splitext(os.path.basename(p).replace("_inst", ""))[0].lower() == t["dll"].lower()), None)
            if not p: return None
            img = NB.F.Image(p); va, size = img.base + t["va"], t["size"]
        seq = N.walk(NB, img, va, size)
    except Exception:
        return None
    if not seq:
        return None
    out = os.path.join(OUT, ident + ".dis.txt")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"; {t['name']} at {t['key']} - instructions in the compiler's block order\n" + "\n".join(seq) + "\n")
    return rel(out)


def has_answer(ident):
    """a real answer exists (older watchers saved failures as .md too: those do not count)"""
    p = os.path.join(OUT, ident + ".md")
    if not os.path.exists(p): return False
    try: return not open(p, encoding="utf-8", errors="replace").read(200).startswith("<!-- local model: request failed")
    except OSError: return False


def collect(targets):
    L = ["# Pre-read targets", "",
         f"Written {time.strftime('%Y-%m-%d %H:%M')} by Tools/localai/preread.py from Tools/next.py. Digests are hints from "
         "the local model about Ghidra's output - check anything you use against the binary.", ""]
    for i, t in enumerate(targets, 1):
        ident = "pre_" + re.sub(r"[^\w.-]+", "_", t["key"])[:50]
        p = os.path.join(OUT, ident + ".md")
        L.append(f"## {i}. {t['name']}  ({t['key']}, {t['size']} bytes, cost {t.get('cost', 0):.1f})")
        L.append(f"File: {t.get('file') or '?'}" + (f"   Closest matched: {t['neighbour']} ({t['sim']:.2f})" if t.get("neighbour") else ""))
        if has_answer(ident):
            text = open(p, encoding="utf-8", errors="replace").read()
            L += ["", re.sub(r"^<!--.*?-->\n", "", text, flags=re.S).strip(), ""]
        else:
            L += ["", f"(digest not here yet: {ident}.md)", ""]
    open(PLAN, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    have = sum(1 for t in targets if has_answer("pre_" + re.sub(r"[^\w.-]+", "_", t["key"])[:50]))
    print(f"{PLAN}: {len(targets)} targets, {have} digests")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=15); ap.add_argument("--folder"); ap.add_argument("--max-size", type=int)
    ap.add_argument("--min-size", type=int, default=64,
                    help="smaller functions are cheaper to read directly than through a digest (default 64 bytes)")
    ap.add_argument("--collect", action="store_true", help="only merge the digests that have arrived into PREREAD.md")
    ap.add_argument("--force", action="store_true", help="ask again even when a digest exists")
    ap.add_argument("--va", nargs="+", metavar="ADDR", help="digests of these functions instead of next.py's list")
    ap.add_argument("--evidence", nargs="+", metavar="ADDR", help="naming evidence for these (placeholder-named) functions")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(QUEUE, exist_ok=True)
    if a.va or a.evidence:
        ev = bool(a.evidence); ids = []; missing = 0
        for tok in (a.evidence or a.va):
            q = build_question(make_target(tok), evidence=ev)
            if q is None:
                missing += 1; print(f"  {tok}: not in Ghidra's output and no disassembly"); continue
            if has_answer(q["id"]) and not a.force:
                ids.append(q["id"] + " (already there)"); continue
            with open(os.path.join(QUEUE, f"ask_{q['id']}.json"), "w", encoding="utf-8") as f:
                json.dump(q, f, indent=1)
            ids.append(q["id"])
        print(f"{len(ids)} questions -> Tools\\localai\\out\\<id>.md: " + ", ".join(ids) + (f"; {missing} not found" if missing else ""))
        return
    if a.collect:
        if not os.path.exists(LIST): sys.exit("no target list yet - run preread.py without --collect first")
        collect(json.load(open(LIST, encoding="utf-8"))); return
    cmd = [sys.executable, os.path.join(ROOT, "Tools", "next.py"), "--top", str(a.top), "--json", LIST]
    if a.folder: cmd += ["--folder", a.folder]
    if a.max_size: cmd += ["--max-size", str(a.max_size)]
    cmd += ["--min-size", str(a.min_size)]
    print("choosing targets (Tools\\next.py) ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode or not os.path.exists(LIST):
        sys.exit("next.py failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    targets = json.load(open(LIST, encoding="utf-8"))
    queued = skipped = missing = 0
    for t in targets:
        q = build_question(t)
        if q is None:
            missing += 1; continue
        if has_answer(q["id"]) and not a.force:
            skipped += 1; continue
        with open(os.path.join(QUEUE, f"ask_{q['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(q, f, indent=1)
        queued += 1
    print(f"{queued} questions queued for the local model, {skipped} already have a digest, "
          f"{missing} not found in Ghidra's output")
    collect(targets)


if __name__ == "__main__":
    main()
