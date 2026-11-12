#!/usr/bin/env python3
"""
batch.py - judge every function of one or more source files in one compact table. Free tool (Tools\\TOOLS.md),
both projects. For rounds that write many small functions (trivial bodies, clusters, a whole class): one command,
one line per function, instead of reading verdict output function by function.

    python3 -I Tools/batch.py gx/gxcanvas.cpp ui/uibutton.cpp --results <staged Results folder>     (Claude's side)
    py Tools\\batch.py TKernelInterface\\TVector3.cpp --host        (PC: build these files on the PC first, then judge)
    py Tools\\batch.py TKernelInterface\\TVector3.cpp               (PC: judge the VM's last build in Results\\)
Options:  --open        only list functions that do not match
          --all         also list compiled functions without a known address (compiler-generated helpers, statics)
          --results DIR where the build is (default Results\\, or Results_host\\ with --host)

Columns: MATCH / DIFF / ?, size of ours vs the original, where the first difference is and how much differs, the
function. "?" = compiled but its address is unknown (not exported, not in Notes\\<...>.map yet).
This is a quick look, not the verdict: it does not count attempts (verdict.py does), JPOG call/data targets are
not re-checked, and host builds are never trusted. A function counts only after a VM build and the anti-cheat.
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
import argparse, difflib, glob, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))


def load_compare():
    import inspect, dis                             # the standard 'dis' first: Zoo has a Tools\dis.py of its own
    try: import capstone                            # noqa: F401
    except Exception: pass
    sys.path.insert(0, HERE)
    import compare as C
    return C


def read_map(path, base=None):
    out = []
    if os.path.exists(path):
        for ln in open(path, errors="replace"):
            ln = ln.split("#", 1)[0].strip()
            if "=" in ln:
                k, v = ln.rsplit("=", 1); v = int(v.strip(), 16 if not v.strip().lower().startswith("0x") else 0)
                out.append((k.strip(), v if base is None or v >= base else v + base))
    return out


def pretty(name):
    """decorated name -> Class::method (constructors, destructors and operator= included)"""
    m = re.match(r"\?\?([0-9]|_[0-9A-Z])([^@]+)@", name)
    if m:
        code, cls = m.groups()
        return {"0": f"{cls}::{cls}", "1": f"{cls}::~{cls}", "4": f"{cls}::operator="}.get(code, name)
    m = re.match(r"\?([^@?]+)@([^@]+)@", name)
    return f"{m.group(2)}::{m.group(1)}" if m else name.lstrip("_")


def aligned_diff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return max(len(a), len(b)) - sum(x.size for x in sm.get_matching_blocks())


def judge_zoo(files, resdir):
    C = load_compare()
    exe = os.path.join(ROOT, "Original", "zoo.exe")
    pe = C.PE(exe); dis = C.Disasm(); orig = C.OrigCode(pe, dis)
    C.enable_symcheck(exe, os.path.join(ROOT, "Notes", "zoo.map"))
    pats = read_map(os.path.join(ROOT, "Notes", "zoo.map"), pe.base)
    def lookup(n):
        for k, v in pats:
            if k == n: return v
        for k, v in pats:
            if k in n: return v
    for p in glob.glob(os.path.join(resdir, "*.obj")) + glob.glob(os.path.join(HERE, "lib", "*.obj")):
        try: C.register_obj(C.Obj(p))                       # callees in other files (post-link pasting)
        except Exception: pass
    rows = []
    for folder, stem in files:
        p = os.path.join(resdir, f"{folder}.{stem}.obj")
        if not os.path.exists(p):
            rows.append(("NOBUILD", "", "", f"{folder}\\{stem}.cpp: no {os.path.basename(p)} in {resdir}")); continue
        obj = C.Obj(p)
        for k, (sec, val, name) in enumerate(obj.funcs):
            _, s, e = obj.func_bytes(k)
            va = lookup(name)
            if va is None:
                rows.append(("?", f"{e - s}", "", pretty(name))); continue
            try:
                C.compare_function(obj, k, va, orig, dis); st, note = "MATCH", ""
            except C.Mismatch as ex:
                st, note = "DIFF", str(ex).splitlines()[0]
            rows.append((st, f"{e - s}", note, f"{pretty(name)}  {va:#x}"))
    return rows


def judge_jpog(files, resdir):
    C = load_compare()
    bins = {}
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True):
        if p.lower().endswith((".dll", ".exe")):
            k = os.path.splitext(os.path.basename(p).replace("_inst", ""))[0]
            if k not in bins or "_inst" in p: bins[k] = p
    loaded, rows = {}, []
    for folder, stem in files:
        p = os.path.join(resdir, f"{folder}.{stem}.txt")
        if not os.path.exists(p):
            rows.append(("NOBUILD", "", "", f"{folder}\\{stem}.cpp: no {os.path.basename(p)} in {resdir}")); continue
        if folder not in bins:
            rows.append(("NOBUILD", "", "", f"no original binary for {folder}")); continue
        if folder not in loaded:
            d, r2o, exports, _ = C.load_dll(bins[folder])
            loaded[folder] = (d, r2o, exports, read_map(os.path.join(ROOT, "Notes", folder + ".map")))
        d, r2o, exports, mp = loaded[folder]
        rel = C.obj_relocs(p[:-4] + ".obj")
        for name, ins in C.parse_dumpbin(p).items():
            if not ins:
                continue
            rva = exports.get(name)
            if rva is None:
                rva = next((v for k, v in mp if k in name), None)
            if rva is None:
                rows.append(("?", "", "", pretty(name))); continue
            status, ours, theirs, first = C.compare(name, ins, d, r2o(rva), rel.get(name), os.path.exists(p[:-4] + ".rel"))
            if status.startswith("MATCH"):
                rows.append(("MATCH", f"{len(ours)}", "", f"{pretty(name)}  {rva:#x}")); continue
            tol = set()
            for r in rel.get(name, ()): tol.update(range(r, r + 4))
            a = bytes(0 if i in tol else x for i, x in enumerate(bytes(ours)))
            size = f"{len(ours)}/{len(theirs)}" if len(ours) != len(theirs) else f"{len(ours)}"
            rows.append(("DIFF", size, f"first difference at +{first:#x}, {aligned_diff(a, bytes(theirs))} bytes differ",
                         f"{pretty(name)}  {rva:#x}"))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="source files relative to Src (folder\\file.cpp)")
    ap.add_argument("--host", action="store_true"); ap.add_argument("--results"); ap.add_argument("--open", action="store_true")
    ap.add_argument("--all", action="store_true", help="also list compiled functions without a known address")
    a = ap.parse_args()
    files = []
    for f in a.files:
        parts = re.split(r"[\\/]", f.strip())
        if parts and parts[0].lower() == "src":
            parts = parts[1:]
        if len(parts) != 2 or not parts[1].lower().endswith((".cpp", ".c")):
            sys.exit(f"{f}: give <folder>\\<file>.cpp, relative to Src")
        files.append((parts[0], os.path.splitext(parts[1])[0]))
    resdir = a.results or os.path.join(ROOT, "Results_host" if a.host else "Results")
    if a.host:
        spec = importlib.util.spec_from_file_location("hostbuild", os.path.join(HERE, "hostbuild", "hostbuild.py"))
        HB = importlib.util.module_from_spec(spec); spec.loader.exec_module(HB)
        cfg = HB.load_config()
        by_folder = {}
        for folder, stem in files:
            by_folder.setdefault(folder, []).append(os.path.join(ROOT, "Src", folder, stem + ".cpp"))
        for folder, paths in by_folder.items():
            HB.build(folder, cfg, outdir=resdir, only=[p for p in paths if os.path.exists(p)])
    rows = (judge_zoo if ZOO else judge_jpog)(files, resdir)
    n = {k: sum(1 for r in rows if r[0] == k) for k in ("MATCH", "DIFF", "?", "NOBUILD")}
    for st, size, note, what in rows:
        if a.open and st == "MATCH" or st == "?" and not a.all:
            continue
        print(f"{st:7} {size:>9}  {what[:72]:72}  {note[:80]}")
    print(f"\n{n['MATCH']} match, {n['DIFF']} differ, {n['?']} without a known address, {n['NOBUILD']} not built"
          + ("  (host build: a quick look only)" if a.host else ""))
    sys.exit(0 if not n["DIFF"] and not n["NOBUILD"] else 1)


if __name__ == "__main__":
    main()
