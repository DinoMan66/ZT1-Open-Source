#!/usr/bin/env python3
"""
classmap.py - recover classes from zoo.exe: vtables, their methods, constructors, and a name guess.

Usage:  python classmap.py Original/zoo.exe --out Notes/classes.csv [--md Notes/classes.md]

vtables  : addresses in .rdata that a function stores into an object ("mov dword ptr [reg+off], imm")
           and that start a run of function pointers.
ctor/dtor: functions doing that store (both constructors and destructors write the vptr).
names    : 1) Class::method strings a slot (or the ctor) references, majority vote;
           2) registrar create functions (Notes/instances_registrars.csv) -> operator new -> ctor;
status   : per slot, from zoo.map / instances_*.csv / libmatch.csv.
"""
import argparse, collections, csv, glob, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Disasm, OrigCode
from dis import blocks

INLINE_MSGS = ("GXCanvas::lock", "GXCanvas::unlockSurface", "GXCanvas::lockRead", "GXCanvas::lockWrite")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("--out", required=True); ap.add_argument("--md")
    a = ap.parse_args()
    pe = PE(a.exe); orig = OrigCode(pe, Disasm())
    inv = {int(r["va"], 16): r for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "inventory.csv")))}
    text = [(pe.base + va, pe.base + va + vs) for n, va, vs, rs, rp, ch in pe.secs if ch & 0x20000000]
    data = [(pe.base + va, pe.base + va + max(vs, rs)) for n, va, vs, rs, rp, ch in pe.secs if not ch & 0x20000000 and n != ".rsrc"]
    in_text = lambda v: any(s <= v < e for s, e in text)
    in_data = lambda v: any(s <= v < e for s, e in data)
    status = {}
    for ln in open(os.path.join(ROOT, "Notes", "zoo.map"), errors="replace"):
        ln = ln.split("#", 1)[0]
        if "=" in ln: status[int(ln.rsplit("=", 1)[1], 0)] = "written"
    for f in glob.glob(os.path.join(ROOT, "Notes", "instances_*.csv")) + [os.path.join(ROOT, "Notes", "libmatch.csv")]:
        if os.path.exists(f):
            for r in csv.DictReader(open(f)):
                if r["status"].startswith("MATCH"): status[int(r["va"], 16)] = "matched"
    def sat(v):
        b = pe.read(v, 96)
        if not b: return None
        z = b.split(b"\0")[0]
        return z.decode("latin1") if len(z) >= 4 and all(32 <= c < 127 for c in z) else None
    # walk every function once: vptr stores, Class:: strings, direct calls
    stores = collections.defaultdict(set)      # vtable -> functions storing it
    cls_strings = collections.defaultdict(collections.Counter)  # function -> Class names in its strings
    calls = collections.defaultdict(set)
    for va in inv:
        seen, _ = blocks(orig, va)
        for x, i in seen.items():
            b = i.b
            if len(b) >= 6 and b[0] == 0xC7 and (b[1] >> 6) in (0, 1, 2) and (b[1] >> 3) & 7 == 0:
                imm = struct.unpack_from("<I", b, len(b) - 4)[0]
                if in_data(imm) and in_text(pe.u32(imm) or 0) and (pe.u32(imm) in inv):
                    stores[imm].add(va)
            if i.kind == "call": calls[va].add(i.target)
            if len(b) >= 5:
                s = sat(struct.unpack_from("<I", b, len(b) - 4)[0])
                if s:
                    if s.startswith(INLINE_MSGS): continue    # messages of inlined helpers
                    m = re.match(r"([A-Z][A-Za-z0-9_]+)::~?[A-Za-z_]", s)
                    if m: cls_strings[va][m.group(1)] += 1
    # vtable slots
    vt = {}
    for t in stores:
        slots = []
        v = t
        while True:
            f = pe.u32(v)
            if f is None or f not in inv: break
            if v != t and v in stores: break       # next vtable starts
            slots.append(f); v += 4
        vt[t] = slots
    # names
    name = {}
    for t, slots in vt.items():
        c = collections.Counter()
        for f in slots + sorted(stores[t]):
            c.update(cls_strings.get(f, {}))
        if c: name[t] = c.most_common(1)[0][0]
    # registrar create functions: push size; call new; ...; jmp/call ctor -> ctor stores vtable
    regs = os.path.join(ROOT, "Notes", "instances_registrars.csv")
    if os.path.exists(regs):
        for r in csv.DictReader(open(regs)):
            cls = r["key"].split("@")[1] if "@" in r["key"] else None
            va = int(r["va"], 16)
            seen, _ = blocks(orig, va)
            for x, i in seen.items():
                if len(i.b) == 5 and i.b[0] == 0x68:
                    fn = struct.unpack_from("<I", i.b, 1)[0]
                    if fn in inv and fn != va:
                        fs, _ = blocks(orig, fn)
                        for y, j in fs.items():
                            for t in vt:
                                if j.kind in ("call", "jmp") and j.target in stores[t]:
                                    name.setdefault(t, cls)
    rows = []
    for t in sorted(vt):
        slots = vt[t]
        done = sum(1 for f in slots if f in status)
        rows.append([f"{t:#x}", name.get(t, ""), len(slots), done,
                     " ".join(f"{f:#x}" for f in sorted(stores[t])), " ".join(f"{f:#x}" for f in slots)])
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["vtable", "name", "slots", "slots_done", "vptr_writers", "slot_functions"]); w.writerows(rows)
    named = sum(1 for r in rows if r[1])
    print(f"{len(rows)} vtables, {named} named, {sum(r[2] for r in rows)} slots")
    if a.md:
        L = ["# Classes recovered from vtables (Tools/classmap.py)", "",
             "| vtable | name guess | slots | done | constructors/destructors |", "|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:60]} |")
        open(a.md, "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    main()
