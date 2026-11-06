#!/usr/bin/env python3
"""
dis.py - print one function of zoo.exe with all its blocks (BBT cold blocks included),
in the order a compiler would have laid them out (entry first, then by address).

Usage:  python dis.py Original\\zoo.exe 0x53C85A [--strings]
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Disasm, OrigCode

def blocks(orig, entry, stop=()):
    seen, starts, work = {}, set([entry]), [entry]
    while work:
        a = work.pop()
        if a in seen: continue
        starts.add(a)
        while True:
            i = orig.at(a)
            if i is None or a in seen: break
            seen[a] = i
            if i.kind == "ret": break
            if i.kind == "jmp":
                if i.target not in stop: work.append(i.target)
                break
            if i.kind == "jcc": work.append(i.target)
            if i.kind == "ijmp":
                b = i.b
                if len(b) == 7 and b[0] == 0xFF and (b[1] & 0xC7) == 0x04:
                    t = struct.unpack_from("<I", b, 3)[0]; n = 0
                    while n < 512:
                        v = orig.pe.u32(t + 4 * n)
                        if v is None or orig.at(v) is None: break
                        work.append(v); n += 1
                break
            a += len(i.b)
    return seen, starts

def main():
    pe = PE(sys.argv[1]); orig = OrigCode(pe, Disasm())
    entry = int(sys.argv[2], 0)
    seen, starts = blocks(orig, entry)
    def sat(v):
        b = pe.read(v, 64).split(b"\0")[0]
        return b.decode() if len(b) >= 3 and all(32 <= c < 127 for c in b) else None
    prev = None
    for a in sorted(seen, key=lambda x: (x < entry, x)):
        i = seen[a]
        if prev is not None and a != prev:
            print(f"  ---- block {a:#x}{'  (cold)' if abs(a - entry) > 0x4000 else ''}")
        s = ""
        if len(i.b) >= 5:
            v = struct.unpack_from("<I", i.b, len(i.b) - 4)[0]
            t = sat(v) if pe.in_image(v) else None
            if t: s = f'   ; "{t}"'
        print(f"  {a:#x}: {i.b.hex(' '):<30} {i.text}{s}")
        prev = a + len(i.b)

if __name__ == "__main__":
    main()
