#!/usr/bin/env python3
"""
regress.py - did a change break something that used to match? Free tool (Tools\\TOOLS.md), both projects.

A shared header is included by many files, so one edit can quietly change functions that already matched.
This tool answers two questions:

  1. Which source files does a header reach?  (so the right folders get rebuilt)
       python3 -I Tools/regress.py --who TVector.h
       python3 -I Tools/regress.py --who uicontrol.h gxcanvas.h

  2. After the rebuild: which functions matched at the last anti-cheat run but do not match now?
       Zoo    python3 -I Tools/regress.py "<staged Results>/*.obj"
       JPOG   python3 -I Tools/regress.py "<staged Results>/*.txt"        (unbundle ALL.txt first, or point at Results\\)
     Exit code 1 and a list when something regressed; "no regressions" otherwise. Only functions present in the
     given build are judged, so build every folder that --who lists.

The reference is Notes\\verified_functions.csv, written by the anti-cheat (the last verified state). The comparison
is the project's own compare.py. It is a quick guard for the working loop, not a verdict: call and data targets
are not re-checked on JPOG, and the anti-cheat remains the judge. Rule (CLAUDE.md): a header change is kept only
when this reports no regressions - otherwise fix or revert it before going on.
Needs capstone or GNU objdump, like the other tools. Idea from decompdecomp's shared-header rule.
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
import argparse, csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
INC = re.compile(r'^[ \t]*#[ \t]*include[ \t]*["<]([^">]+)[">]', re.M)


def who(headers):
    src = os.path.join(ROOT, "Src")
    files = [p for p in glob.glob(os.path.join(src, "**", "*"), recursive=True)
             if os.path.isfile(p) and p.lower().endswith((".h", ".hpp", ".inl", ".c", ".cpp"))]
    inc = {}
    for p in files:
        try:
            t = open(p, encoding="latin1").read()
        except OSError:
            continue
        inc[p] = {os.path.basename(x).lower() for x in INC.findall(t)}
    want = {os.path.basename(h).lower() for h in headers}
    missing = want - {os.path.basename(p).lower() for p in files}
    for m in sorted(missing):
        print(f"(no file called {m} under Src\\)")
    reach = set(want)
    changed = True
    while changed:                                   # headers that include the header, and so on
        changed = False
        for p, names in inc.items():
            b = os.path.basename(p).lower()
            if b not in reach and not p.lower().endswith((".c", ".cpp")) and names & reach:
                reach.add(b); changed = True
    hit = sorted(p for p, names in inc.items() if p.lower().endswith((".c", ".cpp")) and names & reach)
    folders = {}
    for p in hit:
        rel = os.path.relpath(p, src)
        folders.setdefault(rel.split(os.sep)[0] if os.sep in rel else "(Src root)", []).append(rel)
    via = sorted(reach - want)
    print(f"{', '.join(sorted(want))} reaches {len(hit)} source files in {len(folders)} folders"
          + (f" (also through {', '.join(via[:8])}{' ...' if len(via) > 8 else ''})" if via else ""))
    for f in sorted(folders):
        print(f"  {f}: {len(folders[f])} files" + ("" if len(folders[f]) > 6 else "  (" + ", ".join(os.path.basename(x) for x in folders[f]) + ")"))
    print("rebuild: " + (" ".join(sorted(folders)) if folders else "nothing"))


def load_tools():
    import inspect, dis                             # the standard 'dis' first: Zoo has a Tools\dis.py of its own
    try: import capstone                            # noqa: F401
    except Exception: pass
    sys.path.insert(0, HERE)
    import compare as C
    return C


def reference():
    p = os.path.join(ROOT, "Notes", "verified_functions.csv")
    if not os.path.exists(p):
        sys.exit("no Notes\\verified_functions.csv - run the anti-cheat once first")
    ok = {}
    for r in csv.DictReader(open(p, newline="", encoding="utf-8", errors="replace")):
        if r["kind"] == "function" and r["status"] == "MATCH":
            ok[(r["name"], int(r["va"], 16))] = r["source"]
    return ok


def now_zoo(paths):
    C = load_tools()
    exe = os.path.join(ROOT, "Original", "zoo.exe"); mp = os.path.join(ROOT, "Notes", "zoo.map")
    pe = C.PE(exe); dis = C.Disasm(); orig = C.OrigCode(pe, dis)
    C.enable_symcheck(exe, mp)
    pats = []
    for ln in open(mp, errors="replace"):
        ln = ln.split("#", 1)[0].strip()
        if "=" in ln:
            k, v = ln.rsplit("=", 1); v = int(v.strip(), 0); pats.append((k.strip(), v if v >= pe.base else v + pe.base))
    def lookup(n):
        for k, v in pats:
            if k == n: return v
        for k, v in pats:
            if k in n: return v
    objs = {p: C.Obj(p) for p in paths + glob.glob(os.path.join(HERE, "lib", "*.obj"))}
    for o in objs.values():
        C.register_obj(o)
    out = {}
    for p in paths:
        o = objs[p]
        for k, (sec, val, name) in enumerate(o.funcs):
            va = lookup(name)
            if va is None:
                continue
            try:
                C.compare_function(o, k, va, orig, dis); st, note = True, ""
            except C.Mismatch as ex:
                st, note = False, str(ex).splitlines()[0]
            if st or (name, va) not in out:
                out[(name, va)] = (st, note, os.path.basename(p))
    return out


def now_jpog(paths):
    C = load_tools()
    originals = {}
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.dll"), recursive=True) + glob.glob(os.path.join(ROOT, "Original", "*.exe")):
        b = os.path.basename(p).replace("_inst", "").replace(".dll", "").replace(".exe", "")
        if b not in originals or "_inst" in p: originals[b] = p
    out, loaded = {}, {}
    for p in paths:
        b = os.path.basename(p)
        if b.endswith(".compile.txt") or b.count(".") < 2 or b.split(".")[1].startswith("Var") or b in ("ALL.txt", "DONE.txt", "cmd.txt"):
            continue
        dll = b.split(".")[0]
        if dll not in originals:
            continue
        if dll not in loaded:
            d, r2o, exports, _ = C.load_dll(originals[dll])
            base = int.from_bytes(d[int.from_bytes(d[0x3c:0x40], "little") + 0x34:][:4], "little")
            m = {}
            mp = os.path.join(ROOT, "Notes", dll + ".map")
            if os.path.exists(mp):
                for ln in open(mp, errors="replace"):
                    ln = ln.split("#")[0].strip()
                    if "=" in ln:
                        k, v = ln.split("=", 1); m[k.strip()] = int(v.strip(), 16)
            loaded[dll] = (d, r2o, exports, m, base)
        d, r2o, exports, m, base = loaded[dll]
        rel = C.obj_relocs(p[:-4] + ".obj")
        for name, ins in C.parse_dumpbin(p).items():
            if not ins:
                continue
            rva = exports.get(name)
            if rva is None:
                rva = next((v for k, v in m.items() if k in name), None)
            if rva is None:
                continue
            status, ours, theirs, first = C.compare(name, ins, d, r2o(rva), rel.get(name), os.path.exists(p[:-4] + ".rel"))
            st = status.startswith("MATCH")
            key = (name, base + rva)
            if st or key not in out:
                out[key] = (st, "" if st else f"first difference at +{first:#x}", b)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="*", help="built objects (Zoo *.obj) or dumpbin listings (JPOG *.txt)")
    ap.add_argument("--who", nargs="+", metavar="HEADER")
    a = ap.parse_args()
    if a.who:
        who(a.who); return
    if not a.results:
        sys.exit(__doc__)
    paths = sorted({p for pat in a.results for p in (glob.glob(pat) or [pat]) if os.path.isfile(p)})
    if not paths:
        sys.exit("no result files found")
    ref = reference()
    cur = (now_zoo if ZOO else now_jpog)(paths)
    judged = [k for k in cur if k in ref]
    bad = [(k, cur[k]) for k in judged if not cur[k][0]]
    gained = [k for k in cur if cur[k][0] and k not in ref]
    print(f"{len(cur)} functions in this build; {len(judged)} of them matched at the last anti-cheat run")
    if gained:
        print(f"newly matching (not yet verified by the anti-cheat): {len(gained)}")
    if not bad:
        print("no regressions"); return
    print(f"REGRESSIONS: {len(bad)} functions matched before and do not match now")
    for (name, va), (st, note, f) in sorted(bad, key=lambda x: x[1][2])[:80]:
        print(f"  {va:#x}  {name[:70]}  [{f}]  {note[:90]}")
    if len(bad) > 80:
        print(f"  ... {len(bad) - 80} more")
    sys.exit(1)


if __name__ == "__main__":
    main()
