#!/usr/bin/env python3
"""
next.py - which functions to write next: the cheapest unwritten ones first. Free tool (Tools\\TOOLS.md), both projects.

A session should start with a short list, not by exploring. next.py ranks every function that is not matched,
not parked and not out of budget by an ESTIMATED cost, so the cheap ones come first:

    python3 -I Tools/next.py                     the 20 cheapest (Claude's side; py Tools\\next.py on the PC)
    python3 -I Tools/next.py --top 40 --folder gx            Zoo: only functions that belong in Src\\gx
    python3 -I Tools/next.py --folder TKernelInterface       JPOG: only that DLL
    python3 -I Tools/next.py --max-size 200 --json Tools/localai/next.json   (the list for pre-reading)
Options:  --deep N   how many of the best candidates get the slow checks (default 120): their callees and their
                     nearest matched neighbour (neighbours.py)
          --all      also list functions in OPEN_WALLS.md and functions out of retry budget

What the estimate uses (all of it from files the tools already keep; nothing is a verdict):
  size          bytes of original code (Zoo: plus cold blocks the post-link optimizer moved away)
  name          naming evidence: an exported name (JPOG), Notes\\zoo.map, an assert string "Class::method"
                (Zoo inventory), a vtable slot of a named class. Without evidence a match only reaches the
                placeholder tier (not counted as readable), so such functions rank far lower
  class         how many methods of the same class already match (layout and idioms known)
  callees       calls to functions without a name make the result 'partial' or need naming work first
  neighbour     similarity of the original code to an already-matched function (copy its shape)
  history       earlier unmatched attempts (Notes\\attempts.csv) make it dearer
The cost is relative (a ranking), not a number of rounds. The suggested file is where the source probably goes.
Needs capstone or GNU objdump for the deep checks, like neighbours.py; a cache of the matched functions' code is
kept in .cache\\ in the project folder (outside Src/Tools/Notes, so never published).
"""
import os as _os, sys as _sys
# Run as `py Tools\\x.py`, Python puts Tools\\ first on the path, and the project's own Tools\\dis.py then hides the
# standard 'dis' module: capstone (through inspect) fails to load and the tool falls back to objdump. Load the
# standard modules before Tools\\ can shadow them.
_sys.path[:] = [_p for _p in _sys.path if _os.path.abspath(_p or ".") != _os.path.dirname(_os.path.abspath(__file__))]
import inspect, dis  # noqa: E401,F401
try:
    import capstone  # noqa: F401
except Exception:
    pass
import argparse, csv, glob, importlib.util, json, math, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
CACHE = os.path.join(ROOT, ".cache")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def rows(path):
    if not os.path.exists(path):
        return []
    return list(csv.DictReader(open(path, newline="", encoding="utf-8", errors="replace")))


def class_of(sym):
    """decorated or plain name -> class name (or None)"""
    if not sym:
        return None
    m = re.match(r"\?\?(?:[0-9]|_[0-9A-Z])([^@]+)@", sym)
    if m: return m.group(1)
    m = re.match(r"\?[^@?]+@([^@]+)@", sym)
    if m: return m.group(1)
    m = re.match(r"([A-Za-z_]\w*)::", sym)
    return m.group(1) if m else None


def pretty(sym):
    """decorated name -> Class::method (constructors, destructors, operators included)"""
    if not sym: return ""
    m = re.match(r"\?\?([0-9]|_[0-9A-Z])([^@]+)@", sym)
    if m:
        code, cls = m.groups()
        return {"0": f"{cls}::{cls}", "1": f"{cls}::~{cls}", "4": f"{cls}::operator=", "_G": f"{cls}::`scalar deleting dtor'",
                "_E": f"{cls}::`vector deleting dtor'"}.get(code, f"{cls}::operator{code}")
    m = re.match(r"\?([^@?]+)@([^@]+)@", sym)
    return f"{m.group(2)}::{m.group(1)}" if m else sym.lstrip("_?").split("@")[0]


_CLASS_FILES = None

def class_file(cls, folder=None):
    """the Src file that already defines most methods of cls (None if no file has any)"""
    global _CLASS_FILES
    if _CLASS_FILES is None:
        _CLASS_FILES = defaultdict(Counter)
        for p in glob.glob(os.path.join(ROOT, "Src", "*", "*.cpp")):
            if os.path.basename(os.path.dirname(p)).lower() == "zzperm": continue
            try: text = open(p, encoding="latin1").read()
            except OSError: continue
            for m in re.finditer(r"\b([A-Za-z_]\w*)::~?[A-Za-z_]\w*\s*\(", text):
                _CLASS_FILES[m.group(1)][os.path.relpath(p, os.path.join(ROOT, "Src"))] += 1
    files = _CLASS_FILES.get(cls)
    if not files: return None
    if folder:
        inside = Counter({f: n for f, n in files.items() if f.split(os.sep)[0].lower() == folder.lower()})
        if inside: files = inside
    return files.most_common(1)[0][0]


def walls():
    """addresses and names listed in Notes\\OPEN_WALLS.md"""
    vas, names = set(), set()
    p = os.path.join(ROOT, "Notes", "OPEN_WALLS.md")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8", errors="replace"):
            if ln.startswith("|"):
                cells = [c.strip() for c in ln.strip("|\n").split("|")]
                if len(cells) >= 2:
                    names.add(cells[0])
                    for m in re.finditer(r"0x[0-9a-fA-F]+", cells[1]): vas.add(int(m.group(0), 16))
    return vas, names


# ------------------------------------------------------------------------------------------- code (deep checks)
CALL = re.compile(r"^call\s+(?:0x)?([0-9a-f]{4,8})$")


def walk(NB, img, va, size=None, limit=2000):
    """-> raw instruction texts of the function (linear for JPOG, along branches for Zoo, like neighbours.py)"""
    out = []
    if size:
        a, end = va, va + size
        while a < end and len(out) < limit:
            ins = img.at(a)
            if ins is None: break
            ln, text = ins
            if not NB.PADDING.match(text.lower()): out.append(text.lower())
            a += ln
        return out
    seen, work, found = set(), [va], []
    while work and len(found) < limit:
        a = work.pop()
        while len(found) < limit and a not in seen:
            ins = img.at(a)
            if ins is None: break
            seen.add(a); ln, text = ins; text = text.lower()
            found.append((a, text))
            mn = text.split(" ")[0]
            if mn in ("ret", "retn") or mn == "jmp" and not re.match(r"^jmp (0x)?[0-9a-f]{5,8}$", text): break
            m = re.match(r"^(j[a-z]+) (?:0x)?([0-9a-f]{5,8})$", text)
            if m:
                t = int(m.group(2), 16)
                if m.group(1) == "jmp": a = t; continue
                work.append(t)
            a += ln
    return [t for _, t in sorted(found, key=lambda x: (x[0] < va, x[0]))]


def pool_grams(NB, key, pool, code):
    """3-gram profiles of the matched functions, cached against verified_functions.csv"""
    vf = os.path.join(ROOT, "Notes", "verified_functions.csv")
    stamp = f"{os.path.getsize(vf)}-{int(os.path.getmtime(vf))}" if os.path.exists(vf) else "none"
    path = os.path.join(CACHE, f"next_pool_{key}.json")
    try:
        c = json.load(open(path, encoding="utf-8"))
        if c.get("stamp") == stamp:
            return {int(k): (n, Counter({tuple(g.split("¶")): v for g, v in d.items()})) for k, (n, d) in c["pool"].items()}
    except Exception:
        pass
    out = {}
    for va, name in pool.items():
        seq = [NB.norm(t) for t in code(va)]
        out[va] = (name, NB.grams(seq))
    try:
        os.makedirs(CACHE, exist_ok=True)
        json.dump({"stamp": stamp, "pool": {str(va): (n, {"¶".join(g): v for g, v in gr.items()})
                                             for va, (n, gr) in out.items()}}, open(path, "w", encoding="utf-8"))
    except OSError:
        pass
    return out


def nearest(NB, seq, grams_pool):
    g = NB.grams([NB.norm(t) for t in seq])
    best = (0.0, None)
    for va, (name, pg) in grams_pool.items():
        s = NB.cosine(g, pg)
        if s > best[0]: best = (s, name)
    return best


# ------------------------------------------------------------------------------------------- Zoo Tycoon
def zoo_candidates():
    vf = rows(os.path.join(ROOT, "Notes", "verified_functions.csv"))
    done = {int(r["va"], 16) for r in vf if r["status"].endswith("MATCH") and r["va"].startswith("0x")}
    matched_names = {int(r["va"], 16): r["name"] for r in vf if r["kind"] == "function" and r["status"] == "MATCH"}
    att = {}
    for r in rows(os.path.join(ROOT, "Notes", "attempts.csv")):
        try: att[int(r["addr"], 16)] = r
        except ValueError: pass
    names = {}
    for ln in open(os.path.join(ROOT, "Notes", "zoo.map"), errors="replace"):
        ln = ln.split("#", 1)[0].strip()
        if "=" in ln:
            k, v = ln.rsplit("=", 1)
            try: v = int(v.strip(), 0)
            except ValueError: continue
            names[v if v >= 0x400000 else v + 0x400000] = k.strip()
    slot_class = {}
    for r in rows(os.path.join(ROOT, "Notes", "classes.csv")):
        if r.get("name"):
            for x in r.get("slot_functions", "").split():
                try: slot_class.setdefault(int(x, 16), r["name"])
                except ValueError: pass
    per_class = Counter(class_of(n) for n in matched_names.values() if class_of(n))
    wall_vas, _ = walls()
    src = {os.path.normcase(os.path.relpath(p, os.path.join(ROOT, "Src"))): os.path.relpath(p, os.path.join(ROOT, "Src"))
           for p in glob.glob(os.path.join(ROOT, "Src", "*", "*.cpp"))}
    out = []
    for r in rows(os.path.join(ROOT, "Notes", "inventory.csv")):
        va = int(r["va"], 16)
        if va in done: continue
        size = int(r["size"] or 0); cold = int(r["cold_bytes"] or 0); blocks = int(r["blocks"] or 1)
        if size <= 1: continue                                     # shared one-byte stubs
        a = att.get(va, {})
        st = a.get("status", "")
        if st == "matched": continue
        parked = st == "limited" or va in wall_vas
        s = r.get("strings", "")
        m = re.search(r"\b([A-Z]\w+)::(~?\w+)\b", s)
        string_name = f"{m.group(1)}::{m.group(2)}" if m else None
        pm = re.search(r"[A-Za-z]:\\aqua\\src\\(\w+)\\(\w+)\.cpp", s, re.I)
        file = None
        if pm:
            rel = os.path.normcase(os.path.join(pm.group(1), pm.group(2) + ".cpp"))
            file = src.get(rel, f"{pm.group(1).lower()}\\{pm.group(2).lower()}.cpp (new)")
        name = names.get(va) or string_name
        if name and name.startswith("?"): name = pretty(name)          # zoo.map keys are parts of decorated names
        cls = class_of(name) or slot_class.get(va)
        if file is None and cls:
            file = class_file(cls)
            if file is None:
                for rel, real in src.items():
                    if os.path.splitext(os.path.basename(rel))[0] == cls.lower():
                        file = real; break
        evidence = "map" if va in names else "string" if string_name else "vtable" if va in slot_class else ""
        out.append(dict(va=va, key=f"{va:#x}", size=size + cold, name=name or (f"{cls}::?" if cls else f"f{va:x}"),
                        cls=cls, evidence=evidence, class_done=per_class.get(cls, 0) if cls else 0,
                        attempts=int(a.get("attempts") or 0) if st == "open" else 0, parked=parked,
                        file=file or "", extra=1.1 if cold else 1.0, blocks=blocks))
    return out, names, matched_names


def zoo_deep(cands, names, matched_names, deep):
    NB = load("neighbours_tool", os.path.join(HERE, "neighbours.py"))
    F = NB.F
    img = F.Image(os.path.join(ROOT, "Original", "zoo.exe"))
    known = set(names) | set(matched_names)
    for c in cands:
        if c["evidence"] in ("map", "string"): known.add(c["va"])
    pool = pool_grams(NB, "zoo", matched_names, lambda va: walk(NB, img, va))
    for c in cands[:deep]:
        seq = walk(NB, img, c["va"])
        calls = {int(m.group(1), 16) for t in seq for m in [CALL.match(t)] if m}
        c["callees"] = len(calls); c["unnamed"] = sum(1 for x in calls if x not in known)
        c["sim"], c["neighbour"] = nearest(NB, seq, pool)


# ------------------------------------------------------------------------------------------- JPOG
def jpog_candidates():
    vf = rows(os.path.join(ROOT, "Notes", "verified_functions.csv"))
    done = {(r["source"].split("/")[0].lower(), r["name"]) for r in vf if r["status"] == "MATCH"}
    per_class = Counter(class_of(n) for _, n in done if class_of(n))
    att = {}
    for r in rows(os.path.join(ROOT, "Notes", "attempts.csv")):
        att[(os.path.splitext(r["module"])[0].lower().replace("_inst", ""), r["name"])] = r
    wall_vas, wall_names = walls()
    out = []
    for r in rows(os.path.join(ROOT, "Notes", "function_tracker.csv")):
        dll = os.path.splitext(r["dll"])[0]; k = dll.lower().replace("_inst", "")
        dec = r["decorated_name"] or r["name"]
        if (k, dec) in done or r["status"] == "matched": continue
        a = att.get((k, dec), {})
        st = a.get("status", "")
        if st == "matched": continue
        rva = int(r["rva"], 16); size = int(r["max_size_bytes"] or 0)
        if size <= 0: continue
        cls = class_of(dec)
        parked = st == "limited" or r["status"] == "limited" or any(dec.find(w) >= 0 or (cls and w.endswith("::" + (r["name"] or "")))
                                                                     for w in wall_names if w)
        file = ""
        if cls:
            file = class_file(cls, dll) or ""
            if file and not file.lower().startswith(dll.lower() + os.sep): file = ""
        if cls and not file:
            for p in glob.glob(os.path.join(ROOT, "Src", dll, "*.cpp")):
                if os.path.splitext(os.path.basename(p))[0].lower() == cls.lower():
                    file = os.path.relpath(p, os.path.join(ROOT, "Src")); break
            if not file:
                file = f"{dll}\\{cls}.cpp (new)"
        pretty_name = pretty(dec) if dec.startswith("?") else (f"{cls}::{r['name']}" if cls and r["name"] else (r["name"] or dec))
        out.append(dict(va=rva, key=f"{dll} {rva:#x}", dll=dll, k=k, dec=dec, size=size, name=pretty_name, cls=cls,
                        evidence="export" if dec.startswith("?") or r["name"] else "",
                        class_done=per_class.get(cls, 0) if cls else 0,
                        attempts=int(a.get("attempts") or 0) if st == "open" else 0, parked=parked,
                        file=file, extra=1.0, mismatch=r["status"] == "mismatch"))
    return out


def jpog_deep(cands, deep):
    NB = load("neighbours_tool", os.path.join(HERE, "neighbours.py"))
    F = NB.F
    bins = {}
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True):
        if p.lower().endswith((".dll", ".exe")):
            k = os.path.splitext(os.path.basename(p).replace("_inst", ""))[0].lower()
            if k not in bins or "_inst" in p: bins[k] = p
    tracker = rows(os.path.join(ROOT, "Notes", "function_tracker.csv"))
    named = defaultdict(set); sizes = {}
    for r in tracker:
        k = os.path.splitext(r["dll"])[0].lower().replace("_inst", "")
        rva = int(r["rva"], 16); named[k].add(rva); sizes[(k, rva)] = int(r["max_size_bytes"] or 0) or None
    vf = rows(os.path.join(ROOT, "Notes", "verified_functions.csv"))
    images, pools = {}, {}
    for c in cands[:deep]:
        k = c["k"]
        if k not in bins: continue
        if k not in images:
            images[k] = img = F.Image(bins[k])
            pool = {}
            for r in vf:
                if r["kind"] == "function" and r["status"] == "MATCH" and r["source"].split("/")[0].lower() == k:
                    rva = int(r["va"], 16) - img.base
                    pool[rva] = r["name"]; named[k].add(rva)
            pools[k] = pool_grams(NB, k, pool, lambda rva, img=img, k=k: walk(NB, img, img.base + rva, sizes.get((k, rva)) or 400))
        img = images[k]
        seq = walk(NB, img, img.base + c["va"], c["size"])
        calls = {int(m.group(1), 16) - img.base for t in seq for m in [CALL.match(t)] if m}
        c["callees"] = len(calls); c["unnamed"] = sum(1 for x in calls if x not in named[k])
        c["sim"], c["neighbour"] = nearest(NB, seq, pools[k])


# ------------------------------------------------------------------------------------------- the estimate
def base_cost(c):
    x = math.sqrt(max(c["size"], 4)) * c["extra"]
    # without naming evidence a match only reaches the placeholder tier, which does not count as readable
    x *= {"map": 0.8, "string": 0.8, "export": 0.8, "vtable": 1.0}.get(c["evidence"], 2.5)
    x *= 1 - min(c["class_done"], 10) * 0.03
    x *= 1 + 0.25 * c["attempts"]
    if c.get("mismatch"): x *= 1.15                      # written once already and did not match
    return x


def full_cost(c):
    x = c["base"]
    if "sim" in c:
        x *= 1 + 0.15 * c["unnamed"]
        x *= 1.3 - 0.6 * c["sim"]
    return x


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=20); ap.add_argument("--deep", type=int, default=120)
    ap.add_argument("--folder", help="Zoo: Src folder (gx, ui, ...); JPOG: the DLL (TKernelInterface, SimJP, ...)")
    ap.add_argument("--max-size", type=int); ap.add_argument("--min-size", type=int, default=0)
    ap.add_argument("--all", action="store_true", help="also list parked functions (open walls, out of budget)")
    ap.add_argument("--json", help="also write the list to this file (for Tools/localai/preread.py)")
    a = ap.parse_args()
    if ZOO:
        cands, names, matched_names = zoo_candidates()
    else:
        cands = jpog_candidates()
    total = len(cands)
    if not a.all: cands = [c for c in cands if not c["parked"]]
    if a.folder:
        f = a.folder.lower()
        cands = [c for c in cands if (c["file"].lower().replace("/", "\\").startswith(f + "\\") if ZOO else c["k"] == f.replace("_inst", ""))]
    cands = [c for c in cands if c["size"] >= a.min_size and (not a.max_size or c["size"] <= a.max_size)]
    for c in cands: c["base"] = base_cost(c)
    cands.sort(key=lambda c: c["base"])
    deep = min(a.deep, len(cands))
    if deep:
        print(f"checking callees and neighbours of the best {deep} of {len(cands)} candidates ...", file=sys.stderr, flush=True)
        try:
            if ZOO: zoo_deep(cands, names, matched_names, deep)
            else: jpog_deep(cands, deep)
        except FileNotFoundError as ex:                     # neither capstone nor objdump on this PC
            for c in cands:
                for k in ("sim", "neighbour", "callees", "unnamed"): c.pop(k, None)
            print(f"  no disassembler, so ranked without the callee/neighbour checks:\n  {ex}", file=sys.stderr)
    for c in cands: c["cost"] = full_cost(c)
    head = sorted(cands[:deep], key=lambda c: c["cost"]) + cands[deep:]
    show = head[:a.top]
    print(f"{'cost':>5} {'size':>5}  {'function':44} {'name from':8} {'class':>5} {'calls':>7} {'neighbour':>26}  file")
    for c in show:
        calls = f"{c['callees'] - c['unnamed']}/{c['callees']}" if "callees" in c else ""
        nb = f"{c['sim']:.2f} {c.get('neighbour') and pretty(c['neighbour']).split('::')[-1][:20] or ''}" if "sim" in c else ""
        what = (c["key"] + "  " + c["name"]) if ZOO else (c["dll"] + " " + c["name"])
        print(f"{c['cost']:5.1f} {c['size']:5}  {what[:44]:44} {c['evidence'] or '-':8} {c['class_done']:5} {calls:>7} {nb:>26}  {c['file']}"
              + ("  [PARKED]" if c["parked"] else "") + (f"  [{c['attempts']} tries]" if c["attempts"] else ""))
    print(f"\n{len(show)} of {len(cands)} candidates shown ({total} unwritten in all). cost: lower = cheaper (relative); "
          "class: methods of that class already matched; calls: named/all callees; neighbour: similarity to the "
          "closest matched function (neighbours.py shows its source).")
    if a.json:
        keep = ("key", "va", "size", "name", "cls", "evidence", "file", "cost", "sim", "neighbour", "callees", "unnamed", "dll", "dec")
        json.dump([{k: c[k] for k in keep if k in c} for c in show], open(a.json, "w", encoding="utf-8"), indent=1)
        print(f"list written to {a.json}")


if __name__ == "__main__":
    main()
