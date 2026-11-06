#!/usr/bin/env python3
"""
inventory.py - list every function in zoo.exe (recursive descent, BBT-aware).

Usage:  python inventory.py Original\\zoo.exe Notes\\inventory.csv [objdump_listing.asm]

Entry points come from: direct call targets, code pointers stored in .rdata/.data (vtables,
callback tables), immediate operands that point at code (push/mov offset), and the PE entry.
Each function is walked through its control flow (cold blocks included) until ret / tail jump.

Columns: va, size, blocks, cold_bytes (bytes outside the entry's own run), callers,
         found_by, vtable_refs, strings (first string literals the function references)
"""
import csv, re, struct, sys, subprocess, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Insn

def linear(pe, listing=None):
    if listing is None:
        listing = subprocess.run(["objdump", "-d", "-w", "-M", "intel", pe_path], capture_output=True,
                                 text=True).stdout.splitlines()
    out = {}
    for ln in listing:
        m = re.match(r"^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(.*)$", ln)
        if m:
            a = int(m.group(1), 16); b = bytes.fromhex(m.group(2).replace(" ", ""))
            out[a] = Insn(a, b, m.group(3).strip())
    return out

def main():
    global pe_path
    pe_path, out_csv = sys.argv[1], sys.argv[2]
    pe = PE(pe_path)
    listing = open(sys.argv[3]).read().splitlines() if len(sys.argv) > 3 else None
    ins = linear(pe, listing)
    # the linear sweep loses sync after jump tables: decode missed call targets from their entry
    from compare import Disasm, OrigCode
    from dis import blocks
    orig = OrigCode(pe, Disasm())
    for _ in range(3):
        missed = {i.target for i in list(ins.values()) if i.kind in ("call", "jmp", "jcc")
                  and i.target not in ins and pe.off(i.target) is not None
                  and any(s <= i.target < e for s, e in [(pe.base + va, pe.base + va + vs) for n, va, vs, rs, rp, ch in pe.secs if ch & 0x20000000])}
        if not missed: break
        for t in missed:
            seen, _ = blocks(orig, t)
            for a, i in seen.items():
                ins.setdefault(a, i)
    text = [(pe.base + va, pe.base + va + vs) for n, va, vs, rs, rp, ch in pe.secs if ch & 0x20000000]
    data = [(pe.base + va, pe.base + va + max(vs, rs), n) for n, va, vs, rs, rp, ch in pe.secs if not ch & 0x20000000]
    in_text = lambda v: any(s <= v < e for s, e in text)
    entries = collections.defaultdict(set); callers = collections.Counter(); vtrefs = collections.Counter()
    ep = pe.base + struct.unpack_from("<I", pe.d, struct.unpack_from("<I", pe.d, 0x3c)[0] + 40)[0]
    entries[ep].add("entry")
    for a, i in ins.items():
        if i.kind == "call" and i.target in ins:
            entries[i.target].add("call"); callers[i.target] += 1
    # code pointers in data sections (vtables: runs of consecutive code pointers)
    for s, e, n in data:
        if n == ".rsrc": continue
        run = []
        for va in range(s, e - 3, 4):
            v = pe.u32(va)
            if v is not None and in_text(v) and v in ins:
                run.append(v)
            else:
                if run:
                    for v2 in run:
                        entries[v2].add("vtable" if len(run) >= 3 else "dataptr"); vtrefs[v2] += 1
                run = []
    # immediates that point at code
    for a, i in ins.items():
        if i.kind == "other" and len(i.b) >= 5 and (i.b[0] == 0x68 or 0xB8 <= i.b[0] <= 0xBF or i.b[0] == 0xC7):
            v = struct.unpack_from("<I", i.b, len(i.b) - 4)[0]
            if in_text(v) and v in ins and v != a:
                entries[v].add("imm")
    # strings
    def string_at(v):
        b = pe.read(v, 80)
        if not b: return None
        z = b.split(b"\0")[0]
        if len(z) >= 4 and all(32 <= c < 127 for c in z):
            return z.decode()
        return None
    E = set(entries)
    rows = []
    for ent in sorted(E):
        seen = set(); work = [ent]; blocks = 0; strs = []
        while work:
            a = work.pop()
            if a in seen or a not in ins: continue
            blocks += 1
            while a in ins and a not in seen:
                i = ins[a]; seen.add(a)
                if i.kind == "other" and len(i.b) >= 5:
                    v = struct.unpack_from("<I", i.b, len(i.b) - 4)[0]
                    if not in_text(v):
                        s = string_at(v)
                        if s and s not in strs and len(strs) < 3: strs.append(s)
                if i.kind == "ret": break
                if i.kind == "jmp":
                    if i.target not in E: work.append(i.target)
                    break
                if i.kind == "jcc":
                    work.append(i.target)
                if i.kind == "ijmp":
                    m = re.search(r"\*4\+0x([0-9a-f]+)\]", i.text)
                    if m:
                        t = int(m.group(1), 16); n = 0
                        while n < 512:
                            v = pe.u32(t + 4 * n)
                            if v is None or not in_text(v) or v not in ins: break
                            work.append(v); n += 1
                    break
                a += len(i.b)
                if a in E and a != ent: break       # ran into the next function
        size = sum(len(ins[x].b) for x in seen)
        run_end = ent
        while run_end in seen: run_end += len(ins[run_end].b)
        cold = sum(len(ins[x].b) for x in seen if not (ent <= x < run_end))
        rows.append([f"{ent:#x}", size, blocks, cold, callers[ent], "+".join(sorted(entries[ent])),
                     vtrefs[ent], " | ".join(strs)])
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["va", "size", "blocks", "cold_bytes", "callers", "found_by", "vtable_refs", "strings"])
        w.writerows(rows)
    print(f"{len(rows)} functions, {sum(r[1] for r in rows)} bytes covered of "
          f"{sum(e - s for s, e in text)} text bytes; {sum(1 for r in rows if r[3])} have cold blocks")

if __name__ == "__main__":
    main()
