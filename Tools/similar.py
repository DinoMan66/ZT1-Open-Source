#!/usr/bin/env python3
"""
similar.py - rank variants of one function by how close they are to the original (difflib ratio over
normalised instruction sequences; cold blocks in address order). For choosing between Var builds; the
real verdict is still compare.py/verdict.py.

Usage:  python similar.py Original/zoo.exe 0x4CAF3B <obj> [<obj> ...] [--name text] [--diff]
"""
import argparse, difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Disasm, OrigCode, Obj
from dis import blocks

MASK = False
def norm(t):
    t = re.sub(r"0x[0-9a-f]+", "N", t.lower())
    t = re.sub(r"\b\d+\b", "N", t)
    t = re.sub(r"\b(e?[abcd]x|[abcd][lh]|e?[sd]i|e?[sb]p)\b", "R", t) if MASK else t
    return re.sub(r"\s+", " ", t).strip()

def ours_seq(obj, k, dis):
    sec, s, e = obj.func_bytes(k)
    raw = obj.sections[sec]["raw"]
    return [norm(t) for a, (ln, t) in sorted(dis.lengths(raw[s:e], s).items()) if raw[a:a + ln] != b"\x90"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("va"); ap.add_argument("objs", nargs="+")
    ap.add_argument("--name", default=""); ap.add_argument("--diff", action="store_true")
    ap.add_argument("--regs", action="store_true", help="ignore register names (structure only)")
    a = ap.parse_args()
    global MASK; MASK = a.regs
    pe = PE(a.exe); dis = Disasm(); orig = OrigCode(pe, dis); va = int(a.va, 0)
    seen, _ = blocks(orig, va)
    oseq = [norm(seen[x].text) for x in sorted(seen, key=lambda x: (x < va, x))]
    for p in a.objs:
        obj = Obj(p)
        ks = [i for i, f in enumerate(obj.funcs) if a.name in f[2]]
        k = max(ks, key=lambda i: obj.func_bytes(i)[2] - obj.func_bytes(i)[1])
        seq = ours_seq(obj, k, dis)
        sm = difflib.SequenceMatcher(None, oseq, seq, autojunk=False)
        print(f"{sm.ratio():.4f}  {os.path.basename(p)}  ({len(seq)} vs {len(oseq)} instructions)")
        if a.diff:
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op != "equal":
                    print(f"   {op:7s} orig {oseq[i1:i2][:4]}  ours {seq[j1:j2][:4]}")

if __name__ == "__main__":
    main()
