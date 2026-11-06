#!/usr/bin/env python3
"""
instances.py - verify functions that are compiled from one shared source many times
(header-defined statics, inline helpers instantiated per translation unit).

Usage:  python instances.py Original/zoo.exe <objs...> --list Notes/instances_registrars.csv [--write]

The list has columns  va,key,status : 'key' is a text that must appear in the name of a symbol our
function relocates against (e.g. 's_className@UIButton@@'). For each row the script tries every object
function (name starting with --prefix, default '_$E') that references that key and compares it with
the original at 'va' (same CFG/BBT-aware comparison as compare.py). --write stores the status column.
"""
import argparse, csv, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Disasm, OrigCode, Obj, compare_function, Mismatch, enable_symcheck

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("objs", nargs="+")
    ap.add_argument("--list", required=True); ap.add_argument("--prefix", default="_$E")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    pe = PE(a.exe); dis = Disasm(); orig = OrigCode(pe, dis)
    enable_symcheck(a.exe)
    funcs = []                      # (obj, k, name, set of referenced symbol names)
    for p in [p for pat in a.objs for p in (sorted(glob.glob(pat)) or [pat])]:
        obj = Obj(p)
        for k, (sec, val, name) in enumerate(obj.funcs):
            if not name.startswith(a.prefix) and a.prefix != "*": continue
            _, s, e = obj.func_bytes(k)
            refs = {obj.syms.get(si, ("",))[0] for va, (si, t) in obj.sections[sec]["rels"].items() if s <= va < e}
            funcs.append((obj, k, name, refs))
    rows = list(csv.DictReader(open(a.list)))
    tally = collections.Counter(); fails = []
    for r in rows:
        va = int(r["va"], 16)
        if r["key"].startswith("@self:"):
            cand = [f for f in funcs if f[2] == r["key"][6:]]
        else:
            cand = [f for f in funcs if any(r["key"] in x for x in f[3])]
        if not cand:
            r["status"] = "no source"; tally["no source"] += 1; continue
        err = None
        for obj, k, name, _ in cand:            # several shapes may reference the key (ctor, dtor, ...)
            try:
                compare_function(obj, k, va, orig, dis); r["status"] = "MATCH"; err = None; break
            except Mismatch as e:
                err = err or str(e).splitlines()[0]
        if err:
            r["status"] = "DIFF"; fails.append((va, r["key"], err))
        tally[r["status"]] += 1
    print(" | ".join(f"{k} {v}" for k, v in tally.most_common()), f"(of {len(rows)})")
    for va, key, msg in fails[:10]:
        print(f"  DIFF {va:#x} {key}: {msg}")
    if a.write:
        with open(a.list, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    main()
