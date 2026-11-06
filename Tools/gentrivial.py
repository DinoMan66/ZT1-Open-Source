"""gentrivial.py - turn the trivial bodies trivial.py recognises (zoo.exe) into compilable C++.

Each function gets a placeholder class Z_<va> with just the members it touches, so the code
matches; rename the class / members once the owner is known (Notes/classes.csv lists vtable slots).
Writes Src/misc/trivial_unowned.cpp. After the build: python3 -I Tools/gentrivial.py --map <obj>
appends the decorated names to Notes/zoo.map.
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trivial as TR, triage_lib as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = {"dword": "int", "word": "short", "byte": "char"}

def gen(img, va, texts, first=b""):
    """-> C++ text or None"""
    last = texts[-1]
    m = re.match(r"^ret(?:n)?(?: 0x([0-9a-f]+))?$", last)
    if not m: return None
    nargs = int(m.group(1) or "0", 16) // 4
    body = texts[:-1]
    cls = f"Z_{va:X}"
    members, decl_extra = [], []
    def args(first=None):
        a = [] if first is None else [first]
        while len(a) < nargs: a.append(f"int a{len(a)+1}")
        return ", ".join(a)
    def member(off, typ, name="m"):
        if off: members.append(f"char pad[{off:#x}];")
        members.append(f"{typ} {name};")
    if not body:
        fn = f"void f({args()}) {{}}"
    elif len(body) == 1:
        s = body[0]
        if s in ("xor eax,eax", "sub eax,eax"): fn = f"int f({args()}) {{ return 0; }}"
        elif s == "mov al,0x1": fn = f"bool f({args()}) {{ return true; }}"
        elif s == "xor al,al": fn = f"bool f({args()}) {{ return false; }}"
        elif s == "or eax,0xffffffff": fn = f"int f({args()}) {{ return -1; }}"
        elif s == "mov eax,ecx": fn = f"void* f({args()}) {{ return this; }}"
        elif first[:1] in (b"\xa1", b"\xa0"):                # load of a global: mov eax/al,[g]
            v = int(s.split(",")[1], 16); t = "int" if first[:1] == b"\xa1" else "char"
            decl_extra.append(f"extern {t} g_{v:x};")
            fn = f"{t} f({args()}) {{ return g_{v:x}; }}"
        elif re.match(r"^mov al,0x([0-9a-f]+)$", s):
            fn = f"char f({args()}) {{ return {int(s.split(',')[1],16):#x}; }}"
        elif re.match(r"^mov eax,0x([0-9a-f]+)$", s):
            v = int(s.split(",")[1], 16)
            if img.in_image(v):
                decl_extra.append(f"extern int g_{v:x};")
                fn = f"int* f({args()}) {{ return &g_{v:x}; }}"
            else:
                fn = f"int f({args()}) {{ return {v if v < 0x10000 else hex(v)}; }}"
        else:
            mm = re.match(r"^mov (eax|al|ax),(dword|byte|word) \[ecx(?:\+0x([0-9a-f]+))?\]$", s)
            mf = re.match(r"^fld (dword|qword) \[ecx(?:\+0x([0-9a-f]+))?\]$", s)
            ml = re.match(r"^lea eax,\[ecx\+0x([0-9a-f]+)\]$", s)
            ms = re.match(r"^mov (dword|byte|word) \[ecx(?:\+0x([0-9a-f]+))?\],0x([0-9a-f]+)$", s)
            if mm:
                t = W[mm.group(2)]; member(int(mm.group(3) or "0", 16), t)
                fn = f"{t} f({args()}) {{ return m; }}"
            elif mf:
                t = "float" if mf.group(1) == "dword" else "double"; member(int(mf.group(2) or "0", 16), t)
                fn = f"{t} f({args()}) {{ return m; }}"
            elif ml:
                member(int(ml.group(1), 16), "char", "m[1]")
                fn = f"char* f({args()}) {{ return m; }}"
            elif ms:
                t = W[ms.group(1)]; v = int(ms.group(3), 16); member(int(ms.group(2) or "0", 16), t)
                if ms.group(1) == "dword" and img.in_image(v):
                    decl_extra.append(f"extern int g_{v:x};")
                    val = f"(int)&g_{v:x}"
                else:
                    val = hex(v)
                fn = f"void f({args()}) {{ m = {val}; }}"
            else:
                return None
    elif len(body) == 2:
        mm = re.match(r"^mov (eax|ax|al),(?:(dword|word|byte) )?\[esp\+0x4\]$", body[0])
        m2 = re.match(r"^mov (?:(byte|word|dword) )?\[ecx(?:\+0x([0-9a-f]+))?\],(eax|ax|al)$", body[1])
        if not (mm and m2): return None
        t = W[m2.group(1) or {"eax": "dword", "ax": "word", "al": "byte"}[m2.group(3)]]
        member(int(m2.group(2) or "0", 16), t)
        fn = f"void f({args(t + ' v')}) {{ m = v; }}"
    else:
        return None
    head, body_ = fn.split(" {", 1)
    rtype, sig = head.split(" f(", 1)
    out = decl_extra + [f"struct {cls} {{"] + ["    " + x for x in members] + [f"    {rtype} f({sig};", "};",
          f"{rtype} {cls}::f({sig} {{" + body_, ""]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", help="built .obj: append decorated names to Notes/zoo.map")
    a = ap.parse_args()
    if a.map:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import compare as C
        obj = C.Coff(a.map) if hasattr(C, "Coff") else None
        data = open(a.map, "rb").read()
        names = sorted(set(re.findall(rb"\?f@Z_([0-9A-F]+)@@[A-Za-z0-9_@$]+", data)))
        full = sorted(set(re.findall(rb"\?f@Z_[0-9A-F]+@@[A-Za-z0-9_@$]+Z", data)))
        mp = os.path.join(ROOT, "Notes", "zoo.map")
        have = open(mp).read()
        add = []
        for n in full:
            n = n.decode(); va = int(re.match(r"\?f@Z_([0-9A-F]+)@@", n).group(1), 16)
            if n not in have: add.append(f"{n} = {va:#x}")
        open(mp, "a").write("".join(x + "\n" for x in add))
        print(len(add), "map lines added"); return
    class Arg: pass
    parts, n = [], 0
    for img, mod, va, name, st in TR.zoo_functions(Arg()):
        if st != "todo" and not name.startswith("?f@Z_"): continue
        ins, ok = TR.walk(img, va)
        if not ins or not ok: continue
        if not TR.recognise(img, ins): continue
        c = gen(img, va, [T.norm(t) for _, _, t in ins], bytes(ins[0][1]))
        if c: parts.append(f"// {va:#x}\n" + c); n += 1
    hdr = ("// Trivial functions of zoo.exe whose owning class is not known yet (Tools/gentrivial.py).\n"
           "// Z_<va> is a placeholder class holding only the member the function touches; move each\n"
           "// function to its real class when the owner is identified (Notes/classes.csv vtable slots).\n\n#pragma pack(1)\n\n")
    os.makedirs(os.path.join(ROOT, "Src", "misc"), exist_ok=True)
    open(os.path.join(ROOT, "Src", "misc", "trivial_unowned.cpp"), "w").write(hdr + "\n".join(parts))
    print(n, "functions written")

if __name__ == "__main__":
    main()
