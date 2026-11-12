#!/usr/bin/env python3
"""
neighbours.py - before writing a function, see how similar functions that already match were written.
Free tool (Tools\\TOOLS.md), both projects.

It compares the target's ORIGINAL machine code with the original code of every function that already matches
(Notes\\verified_functions.csv, written by the anti-cheat), ranks them by similarity and prints the source of the
closest ones. Copying a matched neighbour's shape is the cheapest way to write a function (decomp.wtf's
"find_similar"; our trivial.py clusters do the same for exact copies only).

Zoo Tycoon:   python3 -I Tools/neighbours.py 0x4CAF3B                   (address of the function to write)
              python3 -I Tools/neighbours.py UIListBox::addItem          (a name from Notes/zoo.map)
JPOG:         python3 -I Tools/neighbours.py TRenderInterface ?Render@TGFXFileInstanceObject   (<Dll> <name or rva>)
              python3 -I Tools/neighbours.py SimJP 0x2f6aa0
Options:      --top N (default 6)   --show N (sources printed, default 2)   --min 0.5 (similarity floor)
              --all   compare with every function in the original binary, not only matched ones (names only)

Similarity: the instruction sequences with registers, numbers and addresses masked (`mov r,[r+N]`), scored as
the share of instructions in the longest common blocks (1.0 = the same shape). A high score means "written the
same way", not "the same function": read the neighbour's source, then write the target in its own terms.
Needs capstone or GNU objdump, like the other tools.
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
import argparse, csv, difflib, glob, importlib.util, os, re, struct, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


F = load("fields_tool", os.path.join(HERE, "fields.py"))                 # its small PE reader + decoder
P = load("permute_tool", os.path.join(HERE, "permuter", "permute.py"))   # its function finder for C++ source


def norm(text):
    """mask what varies between otherwise identical functions (registers, addresses, field offsets, constants) but
    keep what is shape: stack offsets ([esp+8]: which argument) and ret sizes (how many arguments)"""
    t = re.sub(r"\s+", " ", text.lower()).strip()
    t = re.sub(r"(byte|word|dword|qword|tbyte) ptr ", "", t)
    keep = []
    def protect(m):
        keep.append(m.group(0)); return "\u00a7" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[len(keep) - 1 % 26] + "\u00a7"
    t = re.sub(r"\[esp(?:\+(?:0x[0-9a-f]+|\d+))?\]|^retn? (?:0x[0-9a-f]+|\d+)$", protect, t)
    t = re.sub(r"\b(e?[abcd]x|[abcd][lh]|e?[sd]i|e?[sb]p)\b", "r", t)
    t = re.sub(r"0x[0-9a-f]+|\b\d+\b", "n", t)
    for i, v in enumerate(keep):
        t = t.replace("\u00a7" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i % 26] + "\u00a7", v)
    return t


# alignment filler between functions: int3, nop, and the multi-byte "do nothing" forms (lea esi,[esi+eiz*1+0x0])
PADDING = re.compile(r"^(int3|nop\b|xchg\s+ax,\s*ax|mov\s+(e?[ds]i),\s*\2$|lea\s+(e?\w\w),\s*\[\3(\+eiz\*1)?\+0x0\])")


def code_of(img, va, size=None, limit=3000):
    """masked instruction sequence of the function at va: size bytes linearly (JPOG), or along branches (Zoo, whose
    post-link optimizer moved cold blocks away)"""
    out = []
    if size:
        a, end = va, va + size
        while a < end and len(out) < limit:
            ins = img.at(a)
            if ins is None:
                break
            ln, text = ins
            if not PADDING.match(text.lower()):
                out.append(norm(text))
            a += ln
        return out
    seen, work, found = set(), [va], []
    while work and len(found) < limit:
        a = work.pop()
        while len(found) < limit and a not in seen:
            ins = img.at(a)
            if ins is None:
                break
            seen.add(a); ln, text = ins; text = text.lower()
            found.append((a, norm(text)))
            mn = text.split(" ")[0]
            if mn in ("ret", "retn") or mn == "jmp" and not re.match(r"^jmp (0x)?[0-9a-f]{5,8}$", text):
                break
            m = re.match(r"^(j[a-z]+) (?:0x)?([0-9a-f]{5,8})$", text)
            if m:
                t = int(m.group(2), 16)
                if m.group(1) == "jmp":
                    a = t; continue
                work.append(t)
            a += ln
    return [t for _, t in sorted(found, key=lambda x: (x[0] < va, x[0]))]


def grams(seq, n=3):
    return Counter(tuple(seq[i:i + n]) for i in range(max(0, len(seq) - n + 1)))


def cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    return dot / ((sum(v * v for v in a.values()) ** 0.5) * (sum(v * v for v in b.values()) ** 0.5))


def name_parts(sym):
    """decorated name -> C++ spelling used in the source (Class::method), best effort"""
    m = re.match(r"\?\?([0-9]|_[0-9A-Z])([^@]+)@", sym)
    if m:
        code, cls = m.groups()
        return {"0": f"{cls}::{cls}", "1": f"{cls}::~{cls}"}.get(code)   # operators: no simple spelling
    m = re.match(r"\?([^@?]+)@([^@]+)@", sym)
    return f"{m.group(2)}::{m.group(1)}" if m else sym.lstrip("_?").split("@")[0]


def find_source(cpp_name, hint):
    """-> (relative path, first line, body text) of the definition of cpp_name under Src"""
    if not cpp_name:
        return None
    files = glob.glob(os.path.join(ROOT, "Src", "**", "*.cpp"), recursive=True) + \
            glob.glob(os.path.join(ROOT, "Src", "**", "*.h"), recursive=True)
    if hint:                                  # the file the match was built from first: <folder>.<stem>.txt / .obj
        parts = os.path.basename(hint).split(".")
        folder, stem = (parts[0], parts[1]) if len(parts) >= 3 else ("", os.path.splitext(hint)[0])
        want = os.path.normcase(os.path.join(ROOT, "Src", folder, stem))
        files.sort(key=lambda p: (os.path.normcase(os.path.splitext(p)[0]) != want,
                                  os.path.splitext(os.path.basename(p))[0].lower() != stem.lower(),
                                  os.path.dirname(p) == os.path.join(ROOT, "Src")))
    short = cpp_name.split("::")[-1]
    for p in files:
        try:
            t = open(p, encoding="latin1").read()
        except OSError:
            continue
        if short not in t:
            continue
        span = P.find_function(t, cpp_name)
        if span:
            b, e = span
            head_start = t.rfind("\n", 0, t.rfind("(", 0, b)) + 1
            return os.path.relpath(p, ROOT), t.count("\n", 0, head_start) + 1, t[head_start:e + 1]
    return None


# ------------------------------------------------------------------------------------------- the two projects
def zoo_setup(target):
    img = F.Image(os.path.join(ROOT, "Original", "zoo.exe"))
    names = {}
    mp = os.path.join(ROOT, "Notes", "zoo.map")
    for ln in open(mp, errors="replace"):
        ln = ln.split("#", 1)[0].strip()
        if "=" in ln:
            k, v = ln.rsplit("=", 1); v = int(v.strip(), 0); names[v if v >= img.base else v + img.base] = k.strip()
    if re.match(r"^(0x)?[0-9a-fA-F]{5,8}$", target):
        tva = int(target, 16)
    else:
        hits = [va for va, n in names.items() if target.split("::")[-1] in n and
                (("::" not in target) or target.split("::")[0] in n)]
        if not hits:
            sys.exit(f"{target}: not in Notes/zoo.map - give its address")
        tva = hits[0]
    pool = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "verified_functions.csv"), newline="", encoding="utf-8", errors="replace")):
        if r["kind"] == "function" and r["status"] == "MATCH":
            pool[int(r["va"], 16)] = (r["name"], r["source"])
    return img, tva, None, pool, (lambda va: img), (lambda va: None), names


def jpog_setup(dll, target):
    bins = {}
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True):
        if p.lower().endswith((".dll", ".exe")):
            k = os.path.splitext(os.path.basename(p).replace("_inst", ""))[0].lower()
            if k not in bins or "_inst" in p:
                bins[k] = p
    key = dll.lower().replace("_inst", "").replace(".dll", "").replace(".exe", "")
    if key not in bins:
        sys.exit(f"no binary called {dll} under Original\\")
    images = {}
    def image(k):
        if k not in images:
            images[k] = F.Image(bins[k])
        return images[k]
    sizes, names = {}, {}
    for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "function_tracker.csv"), newline="", encoding="utf-8", errors="replace")):
        k = os.path.splitext(r["dll"])[0].lower()
        if k in bins:
            rva = int(r["rva"], 16)
            sizes[(k, rva)] = int(r["max_size_bytes"] or 0) or None
            names[(k, rva)] = r["decorated_name"]
    img = image(key)
    if re.match(r"^(0x)?[0-9a-fA-F]+$", target):
        trva = int(target, 16); trva = trva - img.base if trva >= img.base else trva
    else:
        hits = [rva for (k, rva), n in names.items() if k == key and target in n]
        if not hits:
            sys.exit(f"{target}: no exported function of {dll} contains that text")
        if len(hits) > 1:
            print(f"{len(hits)} functions contain '{target}' - taking the first; give more of the name or the rva:")
            for h in hits[:10]: print(f"   {h:#x}  {names[(key, h)]}")
        trva = hits[0]
    pool = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "verified_functions.csv"), newline="", encoding="utf-8", errors="replace")):
        if r["kind"] == "function" and r["status"] == "MATCH":
            k = r["source"].split("/")[0].lower()
            if k in bins:
                va = int(r["va"], 16)
                pool[(k, va)] = (r["name"], r["source"].split("/")[-1])
    return img, img.base + trva, sizes.get((key, trva)), pool, image, sizes, names, key


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", nargs="+"); ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--show", type=int, default=2); ap.add_argument("--min", type=float, default=0.5)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if ZOO:
        img, tva, tsize, pool, image, sizes, names = zoo_setup(a.what[0])
        target = code_of(img, tva)
        cands = [(va, nm, src, lambda va=va: code_of(img, va)) for va, (nm, src) in pool.items() if va != tva]
        if a.all:
            cands += [(va, nm, "", lambda va=va: code_of(img, va)) for va, nm in names.items() if va not in pool and va != tva]
        label = names.get(tva, f"{tva:#x}")
    else:
        if len(a.what) < 2:
            sys.exit("JPOG: neighbours.py <Dll or SimJP> <name or rva>")
        img, tva, tsize, pool, image, sizes, names, key = jpog_setup(a.what[0], a.what[1])
        target = code_of(img, tva, tsize or 0x400)
        cands = []
        for (k, va), (nm, src) in pool.items():
            if k == key and va == tva:
                continue
            im = image(k)
            cands.append((va, f"{nm}", f"{k}:{src}", lambda im=im, k=k, va=va: code_of(im, va, sizes.get((k, va - im.base)) or 0x400)))
        if a.all:
            for (k, rva), nm in names.items():
                if k == key and img.base + rva != tva and (k, img.base + rva) not in pool:
                    cands.append((img.base + rva, nm, "", lambda rva=rva: code_of(img, img.base + rva, sizes.get((key, rva)) or 0x400)))
        label = names.get((key, tva - img.base), f"{tva:#x}")
    if not target:
        sys.exit(f"no code at {tva:#x}")
    tg = grams(target)
    rough = []
    for va, nm, src, get in cands:
        seq = get()
        if not seq:
            continue
        ratio = min(len(seq), len(target)) / max(len(seq), len(target))
        if ratio < 0.3:
            continue
        rough.append((cosine(tg, grams(seq)) * (0.5 + 0.5 * ratio), va, nm, src, seq))
    meth = lambda n: (re.match(r"\?([^@?]+)@", n) or re.match(r"(\?\?[0-9A-Z_]+)", n) or re.match(r"(.*)", n)).group(1)
    tmeth = meth(label)
    rough.sort(key=lambda r: (-round(r[0], 3), meth(r[2]) != tmeth))
    scored = []
    for c, va, nm, src, seq in rough[:80]:
        sm = difflib.SequenceMatcher(None, target, seq, autojunk=False)
        scored.append((sm.ratio(), va, nm, src, len(seq)))
    # ties: same method name first (another class's GetClass / CreateObjectInPlace is the best model), then matched
    scored.sort(key=lambda r: (-round(r[0], 3), meth(r[2]) != tmeth, not r[3]))
    allscored = [s for s in scored if s[0] >= a.min]
    scored = allscored[:a.top]
    print(f"target {label} at {tva:#x}: {len(target)} instructions; compared with {len(cands)} "
          f"{'functions' if a.all else 'matched functions'}")
    if not scored:
        print(f"nothing above similarity {a.min} - this one has no close matched neighbour"); return
    print(f"\n{'similarity':>10}  {'size':>5}  function")
    for s, va, nm, src, n in scored:
        print(f"{s:10.2f}  {n:5d}  {nm[:90]}  {va:#x}" + (f"  [{src}]" if src else "  (not matched)"))
    shown, looked = 0, set()
    best = scored[0][0]
    # sources: the listed ones first, then equally close ones further down (some matches are written by a macro
    # or in a header and cannot be shown as one plain function)
    show = scored + [x for x in allscored[a.top:] if x[0] >= best - 0.02]
    show.sort(key=lambda r: (-round(r[0], 2), meth(r[2]) != tmeth))       # same method name first
    for s, va, nm, src, n in show:
        if shown >= a.show or not src or (nm, va) in looked:
            continue
        looked.add((nm, va))
        hit = find_source(name_parts(nm), src.split(":")[-1])
        if not hit:
            continue
        rel, line, body = hit
        lines = body.splitlines()
        print(f"\n--- {s:.2f}  {rel}:{line}  ({nm[:70]})")
        print("\n".join(lines[:70]) + (f"\n    ... {len(lines) - 70} more lines" if len(lines) > 70 else ""))
        shown += 1
    if a.show and not shown and any(s[3] for s in scored):
        print("\n(no plain definition found for these matches: they may come from a macro or a header - grep Src for the name)")


if __name__ == "__main__":
    main()
