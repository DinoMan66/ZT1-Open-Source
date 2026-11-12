#!/usr/bin/env python3
"""
fields.py - which fields does a class have? Reads every method of a class in the original binary, follows the
`this` pointer and lists each offset the code touches: size, reads, writes, a type guess and who uses it.
Then drafts the member list with honest placeholder names. Free tool (Tools\\TOOLS.md), both projects.

Zoo Tycoon:   python3 -I Tools/fields.py UIControl            (class name from Notes/classes.csv or zoo.map)
              python3 -I Tools/fields.py 0x62d4b4             (an unnamed class: its vtable address)
JPOG:         python3 -I Tools/fields.py TRenderInterface TViewport       (<Dll or SimJP> <Class>)
Options:      --out FILE   also write the report there (e.g. Notes/classes/UIControl.md)
              --min N      only offsets touched at least N times (default 1)

Which functions count as the class's methods:
  Zoo   the vtable's slot functions and the functions that store the vtable (constructors, destructors) from
        Notes/classes.csv, plus zoo.map names containing ?name@Class@@
  JPOG  every exported non-static function of the class in that binary (Notes/function_tracker.csv)

How it works: `this` arrives in ecx. The tool walks each function along its branches, remembers which registers
hold `this` (copies such as `mov esi,ecx`; a call clears eax/ecx/edx), and records every memory operand
[this+offset]. Limits, so read the result as evidence to check, not as the layout: it does not follow `this`
through the stack or into called functions; inherited methods touch the base class's fields; a field only reached
through another pointer is missed; sizes come from the instruction (a 4-byte access may be an int, a pointer or a
float moved as an integer). Output is a draft for a header written by hand - never paste it into Src unreviewed.
Needs capstone or GNU objdump, like the other tools. Idea from decompdecomp's class recovery.
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
import argparse, collections, csv, glob, os, re, struct, subprocess, sys, tempfile
CAPSTONE_ERROR = None      # why capstone could not be used (shown by the tools that fall back to objdump)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
REGS = {"eax", "ecx", "edx", "ebx", "esi", "edi", "ebp"}
SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "tbyte": 10, "xmmword": 16}
WRITES = {"mov", "add", "sub", "and", "or", "xor", "inc", "dec", "neg", "not", "shl", "shr", "sar", "sal", "rol", "ror",
          "adc", "sbb", "xchg", "fstp", "fst", "fistp", "fist", "pop", "movs", "stos"}
NO_DEST = {"cmp", "test", "push", "call", "jmp", "ret", "retn", "nop", "leave"}
MAX_INSNS = 6000


# ------------------------------------------------------------------------------------------- tiny PE + decoder
class Image:
    def __init__(self, path):
        self.d = d = open(path, "rb").read()
        pe = struct.unpack_from("<I", d, 0x3c)[0]
        self.base = struct.unpack_from("<I", d, pe + 0x34)[0]
        n = struct.unpack_from("<H", d, pe + 6)[0]
        so = pe + 24 + struct.unpack_from("<H", d, pe + 20)[0]
        self.secs = [struct.unpack_from("<8sIIII", d, so + 40 * i) for i in range(n)]
        try:
            import capstone
            self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        except Exception as ex:
            self.cs = None
            global CAPSTONE_ERROR
            CAPSTONE_ERROR = f"{type(ex).__name__}: {ex}"
        self.cache = {}

    def off(self, va):
        r = va - self.base
        for nm, vs, sva, rs, ra in self.secs:
            if sva <= r < sva + max(vs, rs):
                return ra + r - sva
        return None

    def at(self, va):
        """-> (length, text) of the instruction at va, decoded on demand in 256-byte windows"""
        if va in self.cache:
            return self.cache[va]
        o = self.off(va)
        if o is None:
            return None
        code = self.d[o:o + 256]
        if self.cs:
            for i in self.cs.disasm(code[:240], va):
                self.cache.setdefault(i.address, (i.size, f"{i.mnemonic} {i.op_str}".strip()))
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
                f.write(code); tmp = f.name
            try:
                txt = subprocess.run(["objdump", "-D", "-b", "binary", "-m", "i386", "-M", "intel", "-w",
                                      f"--adjust-vma={va:#x}", tmp], capture_output=True, text=True).stdout
            except FileNotFoundError:
                raise FileNotFoundError("neither capstone nor objdump can be used. capstone: "
                                        + (CAPSTONE_ERROR or "not installed (py -m pip install capstone)")) from None
            finally:
                os.unlink(tmp)
            rows = []
            for ln in txt.splitlines():
                m = re.match(r"^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(.*)$", ln)
                if m:
                    rows.append((int(m.group(1), 16), len(m.group(2).split()), m.group(3).strip()))
            for a, ln, t in rows[:-3]:                 # the last few may be cut by the window
                self.cache.setdefault(a, (ln, t))
        return self.cache.get(va)


# ------------------------------------------------------------------------------------------- following `this`
MEM = re.compile(r"(?:(byte|word|dword|qword|tbyte|xmmword)\s+ptr\s+)?(?:[a-z]s:)?\[([^\]]+)\]")
TARGET = re.compile(r"^(?:0x)?([0-9a-f]{5,8})(?:\s|$)")


def split_ops(text):
    m = re.match(r"^(?:(rep[a-z]*|lock)\s+)?([a-z0-9]+)\s*(.*)$", text)
    if not m:
        return "", []
    return m.group(2), [o.strip() for o in m.group(3).split(",")] if m.group(3) else []


def mem_this(expr, state):
    """[esi+0x30] with esi = this -> (0x30, indexed?) ; None when the base is not `this`"""
    e = expr.replace(" ", "")
    parts = re.findall(r"([+-]?)(0x[0-9a-f]+|\d+|[a-z]{2,3}(?:\*\d)?)", e)
    base = idx = None; disp = 0
    for sign, tok in parts:
        if re.match(r"^(0x[0-9a-f]+|\d+)$", tok):
            v = int(tok, 0); disp += -v if sign == "-" else v
        elif "*" in tok:
            idx = tok
        elif base is None:
            base = tok
        else:
            idx = tok
    if base in state and (idx is None or idx.split("*")[0] not in state):
        if 0 <= disp < 0x10000:
            return disp, idx is not None
    if idx in state and base is not None and base not in state and "*" not in (idx or ""):
        if 0 <= disp < 0x10000:                 # [reg+this+N]: this is the second operand
            return disp, True
    return None


def walk(img, entry, record, fname):
    work = [(entry, frozenset({"ecx"}))]
    seen = set(); count = 0
    while work and count < MAX_INSNS:
        a, state = work.pop()
        state = set(state)
        while count < MAX_INSNS:
            if a in seen:
                break
            ins = img.at(a)
            if ins is None:
                break
            seen.add(a); count += 1
            ln, text = ins; text = text.lower()
            mn, ops = split_ops(text)
            fpu = mn.startswith("f")
            for k, op in enumerate(ops):
                m = MEM.search(op)
                if not m:
                    continue
                hit = mem_this(m.group(2), state)
                if hit is None:
                    continue
                off, indexed = hit
                size = SIZE.get(m.group(1) or "", 0)
                if mn == "lea":
                    kind, size = "addr", 0
                elif k == 0 and (mn in WRITES or mn.startswith("set")):
                    kind = "write" if mn in ("mov", "fstp", "fst", "fistp", "fist", "pop") or mn.startswith("set") else "update"
                else:
                    kind = "read"
                record(off, size, kind, fpu, indexed, fname)
            # where is `this` after this instruction?
            if mn == "call":
                state -= {"eax", "ecx", "edx"}
            elif ops and ops[0] in REGS and mn not in NO_DEST:
                if mn == "mov" and len(ops) == 2 and ops[1] in state:
                    state.add(ops[0])
                elif mn == "xchg" and len(ops) == 2 and ops[1] in REGS:
                    a_, b_ = ops[0] in state, ops[1] in state
                    state -= {ops[0], ops[1]}
                    if a_: state.add(ops[1])
                    if b_: state.add(ops[0])
                else:
                    state.discard(ops[0])
            elif mn == "pop" and ops and ops[0] in REGS:
                state.discard(ops[0])
            if mn in ("ret", "retn"):
                break
            if mn.startswith("j"):
                t = TARGET.match(ops[0]) if ops else None
                tgt = int(t.group(1), 16) if t else None
                if mn == "jmp":
                    if tgt is None or not state:
                        break
                    a = tgt; continue
                if tgt is not None:
                    work.append((tgt, frozenset(state)))
            a += ln
    return count


# ------------------------------------------------------------------------------------------- who are the methods
def zoo_methods(what):
    img = Image(os.path.join(ROOT, "Original", "zoo.exe"))
    funcs = collections.OrderedDict()
    rows = list(csv.DictReader(open(os.path.join(ROOT, "Notes", "classes.csv"), newline="", encoding="utf-8", errors="replace")))
    name = what
    hits = [r for r in rows if r["vtable"].lower() == what.lower()] if what.lower().startswith("0x") else \
           [r for r in rows if r["name"].split(" ")[0].lower() == what.lower()]
    share = collections.Counter(f for r in rows for f in set(r["slot_functions"].split()))
    for r in hits:
        name = r["name"] or f"class with vtable {r['vtable']}"
        for i, f in enumerate(r["slot_functions"].split()):
            va = int(f.split("=")[0], 16)
            label = f"slot {i}" + (" (shared by %d classes)" % share[f] if share[f] > 3 else "")
            funcs.setdefault(va, label)
        for f in r["vptr_writers"].split():
            funcs.setdefault(int(f.split("=")[0], 16), "ctor/dtor")
    mp = os.path.join(ROOT, "Notes", "zoo.map")
    if os.path.exists(mp) and not what.lower().startswith("0x"):
        for ln in open(mp, errors="replace"):
            ln = ln.split("#", 1)[0].strip()
            if "=" in ln and re.search(r"@" + re.escape(what) + r"@@|\b" + re.escape(what) + r"::", ln):
                k, v = ln.rsplit("=", 1); v = int(v.strip(), 0)
                funcs[v if v >= img.base else v + img.base] = k.strip()
    return img, name, funcs


def jpog_methods(dll, cls):
    key = dll.lower().replace("_inst", "").replace(".dll", "").replace(".exe", "")
    cands = [p for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.*"), recursive=True)
             if os.path.splitext(os.path.basename(p).replace("_inst", ""))[0].lower() == key
             and p.lower().endswith((".dll", ".exe"))]
    if not cands:
        sys.exit(f"no binary called {dll} under Original\\")
    path = sorted(cands, key=lambda p: "_inst" not in p)[0]
    img = Image(path)
    funcs = collections.OrderedDict()
    for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "function_tracker.csv"), newline="", encoding="utf-8", errors="replace")):
        if os.path.splitext(r["dll"])[0].lower() != key:
            continue
        m = re.match(r"\?(?:\?[0-9A-Z_]+|[^@?]+)@([^@]+)@(?:[^@]+@)*@([A-Z])", r["decorated_name"])
        if not m or m.group(1) != cls or m.group(2) in "CDKLST":          # static members have no `this`
            continue
        funcs[img.base + int(r["rva"], 16)] = r["name"]
    return img, cls, funcs


# ------------------------------------------------------------------------------------------- report
def guess(sizes, fpu, kinds, indexed):
    if not sizes and "addr" in kinds:
        return "(address taken: an embedded object or array starts here)"
    s = max(sizes) if sizes else 0
    if fpu and s == 4: t = "float"
    elif fpu and s == 8: t = "double"
    elif s == 1: t = "unsigned char / bool"
    elif s == 2: t = "short"
    elif s == 4: t = "int or pointer"
    elif s == 8: t = "8 bytes (double / __int64)"
    else: t = f"{s} bytes"
    return t + (" (array?)" if indexed else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", nargs="+"); ap.add_argument("--out"); ap.add_argument("--min", type=int, default=1)
    a = ap.parse_args()
    if ZOO:
        img, name, funcs = zoo_methods(a.what[0])
    else:
        if len(a.what) < 2:
            sys.exit("JPOG: fields.py <Dll or SimJP> <Class>")
        img, name, funcs = jpog_methods(a.what[0], a.what[1])
    if not funcs:
        sys.exit(f"no methods found for {' '.join(a.what)}")
    F = collections.defaultdict(lambda: dict(sizes=set(), kinds=collections.Counter(), fpu=False, idx=False, who=collections.Counter()))
    def record(off, size, kind, fpu, indexed, fname):
        f = F[off]
        if size: f["sizes"].add(size)
        f["kinds"][kind] += 1; f["fpu"] |= fpu and size in (4, 8); f["idx"] |= indexed; f["who"][fname] += 1
    total = 0
    for va, label in funcs.items():
        total += walk(img, va, record, f"{label} {va - (0 if ZOO else img.base):#x}")
    L = [f"# Fields of {name} (draft from Tools/fields.py)", "",
         f"{len(funcs)} methods read ({total} instructions). Evidence to check, not the layout: see the tool's notes "
         "on its limits. Offset 0 is the vtable pointer.", "",
         "| Offset | Size | Reads | Writes | Guess | Used by |", "|---|---|---:|---:|---|---|"]
    offs = sorted(o for o in F if sum(F[o]["kinds"].values()) >= a.min)
    for o in offs:
        f = F[o]; k = f["kinds"]
        who = ", ".join(n for n, _ in f["who"].most_common(3)) + (f" (+{len(f['who']) - 3})" if len(f["who"]) > 3 else "")
        L.append(f"| 0x{o:02X} | {'/'.join(str(s) for s in sorted(f['sizes'])) or '-'} | {k['read'] + k['update']} | "
                 f"{k['write'] + k['update']} | {guess(f['sizes'], f['fpu'], k, f['idx'])} | {who} |")
    L += ["", "## Draft member list", "", "```cpp"]
    pos = 4
    for o in offs:
        if o < 4:
            continue
        f = F[o]; s = max(f["sizes"]) if f["sizes"] else 4
        if o < pos:
            L.append(f"    // 0x{o:02X}: overlaps the member above ({'/'.join(map(str, sorted(f['sizes']))) or 'address'}) - a union, a smaller view or an embedded object")
            continue
        if not f["sizes"]:
            L.append(f"    // 0x{o:02X}: an embedded object or array starts here (its address is taken); size unknown")
            continue
        if o > pos:
            L.append(f"    /* 0x{pos:02X} */ char          m_unk{pos:02X}[0x{o - pos:X}];   // not touched by these methods")
        ctype = {"float": "float        ", "double": "double       "}.get(guess(f["sizes"], f["fpu"], f["kinds"], False),
                 {1: "unsigned char", 2: "short        ", 4: "int          ", 8: "double       "}.get(s, "int          "))
        note = guess(f["sizes"], f["fpu"], f["kinds"], f["idx"])
        L.append(f"    /* 0x{o:02X} */ {ctype} m_unk{o:02X};   // {note}; read {f['kinds']['read'] + f['kinds']['update']}, written {f['kinds']['write'] + f['kinds']['update']}")
        pos = o + (s if s in (1, 2, 4, 8) else 4)
    L += ["```", "", f"Highest offset touched: 0x{max(offs):X} - the object is at least 0x{max(offs) + 1:X} bytes." if offs else "No field access found."]
    text = "\n".join(L) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        open(a.out, "w", encoding="utf-8", newline="\n").write(text)
    print(text)


if __name__ == "__main__":
    main()
