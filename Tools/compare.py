#!/usr/bin/env python3
"""
compare.py - check compiled functions against the original zoo.exe.

zoo.exe was post-processed after linking (Microsoft BBT-style basic-block reordering): rarely
used blocks of a function were moved far away (often megabytes) and jump back, conditions were
inverted, and branch encodings changed between short and near. A flat byte compare would fail
even for perfect source, so this tool compares CONTROL FLOW:

  * it walks our function (from the .obj) block by block, starting at the entry, and walks the
    original in parallel from its address,
  * unconditional jmps that the original added (or removed) between blocks are followed,
  * conditional branches must have the same condition (or the inverted one with the two
    successors swapped); short/near encoding differences are ignored,
  * every other instruction must be byte-identical, except the 4-byte fields the linker patches
    (our .obj relocations): calls, global/import addresses, string literals,
  * switch jump tables are followed entry by entry,
  * every block mapping must be consistent (one of our blocks <-> one original location).

Usage:
  python compare.py Original\\zoo.exe Results\\*.obj --map Notes\\zoo.map [--report FILE] [-v]

  The map file gives the address of each function in the original:
      part-of-decorated-name = 0x4010C7      (VA, or an RVA below the image base; # = comment)

Disassembler: uses the 'capstone' Python module if installed (pip install capstone),
otherwise GNU objdump (on Claude's side).

Result per function:
  MATCH            identical apart from relocations and BBT layout
  MISMATCH         real difference: the report shows our instruction vs. the original's
  NOT FOUND        no map entry
"""
import argparse, glob, os, re, struct, subprocess, sys, tempfile, datetime

# ------------------------------------------------------------------ PE image
class PE:
    def __init__(self, path):
        self.d = d = open(path, "rb").read()
        pe = struct.unpack_from("<I", d, 0x3c)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        optsz = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<I", d, pe + 24 + 28)[0]
        self.size = struct.unpack_from("<I", d, pe + 24 + 56)[0]
        so = pe + 24 + optsz
        self.secs = []
        for i in range(nsec):
            name, vs, va, rs, rp = struct.unpack_from("<8sIIII", d, so + 40 * i)
            ch = struct.unpack_from("<I", d, so + 40 * i + 36)[0]
            self.secs.append((name.rstrip(b"\0").decode(), va, vs, rs, rp, ch))
    def off(self, va):
        r = va - self.base
        for n, sva, vs, rs, rp, ch in self.secs:
            if sva <= r < sva + max(vs, rs):
                return r - sva + rp if r - sva < rs else None
        return None
    def read(self, va, n):
        o = self.off(va)
        return self.d[o:o + n] if o is not None else b""
    def u32(self, va):
        b = self.read(va, 4)
        return struct.unpack("<I", b)[0] if len(b) == 4 else None
    def in_image(self, v):
        return self.base <= v < self.base + self.size

# ------------------------------------------------------------------ disassembler (lengths only)
class Disasm:
    """Returns instruction lengths. Classification is done from the bytes ourselves."""
    def __init__(self):
        try:
            import capstone
            self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        except Exception:
            self.cs = None
    def lengths(self, code, addr):
        """{addr: (length, text)} for a linear sweep of 'code' placed at 'addr'."""
        out = {}
        if self.cs:
            for i in self.cs.disasm(code, addr):
                out[i.address] = (i.size, f"{i.mnemonic} {i.op_str}".strip())
            return out
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            f.write(code); tmp = f.name
        try:
            txt = subprocess.run(["objdump", "-D", "-b", "binary", "-m", "i386", "-M", "intel", "-w",
                                  f"--adjust-vma={addr:#x}", tmp], capture_output=True, text=True).stdout
        finally:
            os.unlink(tmp)
        for ln in txt.splitlines():
            m = re.match(r"^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(.*)$", ln)
            if m:
                out[int(m.group(1), 16)] = (len(m.group(2).split()), m.group(3).strip())
        return out

class Insn:
    __slots__ = ("addr", "b", "text", "kind", "cc", "target")
    def __init__(self, addr, b, text):
        self.addr, self.b, self.text = addr, b, text
        self.kind, self.cc, self.target = classify(addr, b)

def classify(addr, b):
    i = 0
    while i < len(b) and b[i] in (0x66, 0x67, 0xF2, 0xF3, 0x2E, 0x3E, 0x26, 0x36, 0x64, 0x65):
        i += 1
    if i >= len(b):
        return "other", None, None
    op = b[i]; n = len(b)
    if 0x70 <= op <= 0x7F:
        return "jcc", op & 15, addr + n + struct.unpack("<b", b[i + 1:i + 2])[0]
    if op == 0x0F and i + 1 < n and 0x80 <= b[i + 1] <= 0x8F:
        return "jcc", b[i + 1] & 15, addr + n + struct.unpack("<i", b[i + 2:i + 6])[0]
    if 0xE0 <= op <= 0xE3:
        return "jcc", 0x10 + op - 0xE0, addr + n + struct.unpack("<b", b[i + 1:i + 2])[0]
    if op == 0xEB:
        return "jmp", None, addr + n + struct.unpack("<b", b[i + 1:i + 2])[0]
    if op == 0xE9:
        return "jmp", None, addr + n + struct.unpack("<i", b[i + 1:i + 5])[0]
    if op == 0xE8:
        return "call", None, addr + n + struct.unpack("<i", b[i + 1:i + 5])[0]
    if op in (0xC3, 0xC2, 0xCB, 0xCA):
        return "ret", None, None
    if op == 0xFF and i + 1 < n:
        reg = (b[i + 1] >> 3) & 7
        if reg in (4, 5): return "ijmp", None, None
        if reg in (2, 3): return "icall", None, None
    if op == 0xCC:
        return "int3", None, None
    return "other", None, None

class OrigCode:
    def __init__(self, pe, dis):
        self.pe, self.dis, self.cache = pe, dis, {}
    def at(self, va):
        if va not in self.cache:
            code = self.pe.read(va, 256)
            if not code:
                return None
            for a, (ln, t) in self.dis.lengths(code, va).items():
                if a + ln <= va + len(code) and a not in self.cache:
                    self.cache[a] = Insn(a, code[a - va:a - va + ln], t)
                if a > va + 200:
                    break
        return self.cache.get(va)

# ------------------------------------------------------------------ COFF .obj
class Obj:
    def __init__(self, path):
        self.path = path
        d = self.d = open(path, "rb").read()
        nsect, _, symptr, nsyms, optsz = struct.unpack_from("<HIIIH", d, 2)
        strtab = symptr + nsyms * 18
        def sname(raw):
            if raw[:4] == b"\0\0\0\0":
                o = strtab + struct.unpack_from("<I", raw, 4)[0]
                return d[o:d.index(b"\0", o)].decode("latin1")
            return raw.rstrip(b"\0").decode("latin1")
        self.sections = []
        for s in range(nsect):
            h = 20 + optsz + 40 * s
            name = d[h:h + 8].rstrip(b"\0").decode("latin1")
            rs, rp, relp = struct.unpack_from("<III", d, h + 16)
            nrel = struct.unpack_from("<H", d, h + 32)[0]
            ch = struct.unpack_from("<I", d, h + 36)[0]
            raw = d[rp:rp + rs] if rp else b"\0" * rs
            rels = {}
            for k in range(nrel):
                va, si, typ = struct.unpack_from("<IIH", d, relp + 10 * k)
                rels[va] = (si, typ)
            self.sections.append(dict(name=name, raw=raw, rels=rels, ch=ch))
        self.syms, self.funcs = {}, []
        i = 0
        while i < nsyms:
            o = symptr + 18 * i
            name = sname(d[o:o + 8])
            value, secnum, typ, scl, naux = struct.unpack_from("<IhHBB", d, o + 8)
            self.syms[i] = (name, value, secnum, scl)
            if secnum > 0 and (typ >> 4) == 2 and scl in (2, 3):
                self.funcs.append((secnum - 1, value, name))
            i += 1 + naux
        self.funcs.sort()
    def func_bytes(self, k):
        sec, val, name = self.funcs[k]
        end = len(self.sections[sec]["raw"])
        for s2, v2, _ in self.funcs[k + 1:]:
            if s2 == sec and v2 > val:
                end = v2; break
        return sec, val, end

# ------------------------------------------------------------------ the comparison
class Mismatch(Exception):
    pass

def fmt(i):
    return f"{i.addr:#x}: {i.b.hex(' '):<24} {i.text}"

SYMCHECK = None      # relocation-target checker (Tools/symcheck.py ZooChecker), see enable_symcheck()

def enable_symcheck(exe_path, map_path=None):
    """Anti-cheat oracle rule: every relocation of a matched function must reference the same
    target as the original (symbol + offset). Called by every tool that compares."""
    global SYMCHECK
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)              # python -I does not add the script folder
    import symcheck
    if map_path is None:
        map_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Notes", "zoo.map")
    SYMCHECK = symcheck.ZooChecker(sys.modules[__name__], exe_path, map_path)
    return SYMCHECK

class _Ctx:
    """One of our functions being walked; 'ret' = (caller ctx, our address after the call) when the
    original has it inlined by BBT."""
    def __init__(self, obj, k, dis, ret=None):
        self.obj, self.k, self.ret = obj, k, ret
        self.sec, self.start, self.end = obj.func_bytes(k)
        self.S = obj.sections[self.sec]; raw = self.S["raw"]
        self.ours = {a: Insn(a, raw[a:a + ln], t)
                     for a, (ln, t) in dis.lengths(raw[self.start:self.end], self.start).items()
                     if a + ln <= self.end}
        self.relmask = set()
        for va in self.S["rels"]:
            if self.start <= va < self.end:
                self.relmask.update(range(va, va + 4))

def _add_esp(b):
    if len(b) == 3 and b[:2] == b"\x83\xc4": return b[2]
    if len(b) == 6 and b[:2] == b"\x81\xc4": return struct.unpack_from("<I", b, 2)[0]
    return None

def compare_function(obj, k, entry, orig, dis, _depth=0):
    if _depth > 3:
        raise Mismatch("inlining too deep")
    if SYMCHECK is not None and _depth == 0:
        SYMCHECK.reset()
    top = _Ctx(obj, k, dis)
    visited = {}            # (ctx id, our address) -> set of original addresses it was checked against
    work = [(top, top.start, entry)]
    covered = set(); notes = []
    def follow(g, n=16):
        while n:
            gi = orig.at(g)
            if gi is None or gi.kind != "jmp": return g
            g = gi.target; n -= 1
        return g
    steps = 0
    while work:
        ctx, o, g = work.pop()
        while True:
            steps += 1
            if steps > 20000:
                raise Mismatch("comparison too large (BBT copies / inlining)")
            oi = ctx.ours.get(o)
            if oi is None:
                if ctx.start <= o < ctx.end:
                    raise Mismatch(f"our branch lands inside an instruction at {o:#x}")
                notes.append(f"falls off our function at {o:#x}"); break
            key = (id(ctx), o)
            seen = visited.setdefault(key, set())
            if g in seen or any(follow(x) == follow(g) or same_tail(orig, follow(x), follow(g)) for x in seen):
                break
            if len(seen) >= 6:
                raise Mismatch(f"block at our {o:#x} maps to too many original copies")
            gi = orig.at(g)
            if gi is None:
                raise Mismatch(f"original address {g:#x} is not code")
            # the original jumps where we fall through (block moved by BBT)
            if gi.kind == "jmp" and oi.kind != "jmp":
                covered.update(range(g, g + len(gi.b)))
                g = gi.target; continue
            # alignment nops BBT put between moved blocks
            if gi.b == b"\x90" and oi.b != b"\x90":
                covered.add(g); g += 1; continue
            seen.add(g)
            covered.update(range(g, g + len(gi.b)))
            if oi.kind == "jmp":
                external = (oi.addr + 1) in ctx.S["rels"] or not (ctx.start <= oi.target < ctx.end)
                if gi.kind == "jmp":
                    if not external:
                        work.append((ctx, oi.target, gi.target))
                    elif SYMCHECK is not None:
                        SYMCHECK(ctx.obj, ctx.sec, oi, gi)
                    break                        # tail jump to another function: target is relocated
                if external:
                    # tail jump into another function that BBT placed right here: compare it too when
                    # we have it; otherwise the original must continue with a known function
                    tc = tail_callee(ctx.obj, ctx.sec, oi)
                    if tc is not None:
                        cov2, _ = compare_function(tc[0], tc[1], g, orig, dis, _depth + 1)
                        covered.update(cov2)
                    else:
                        if g not in function_entries():
                            raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (tail jump to an unknown function)")
                        if SYMCHECK is not None:
                            SYMCHECK.tail(ctx.obj, ctx.sec, oi, g)
                    break
                o = oi.target; continue          # BBT placed the target right here
            if oi.kind == "jcc":
                if gi.kind != "jcc":
                    raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)}")
                if gi.cc == oi.cc:
                    work.append((ctx, oi.target, gi.target))
                    o += len(oi.b); g += len(gi.b); continue
                if gi.cc < 16 and gi.cc == oi.cc ^ 1:
                    # inverted: our taken path is the original's fall-through and vice versa
                    work.append((ctx, oi.addr + len(oi.b), gi.target))
                    o = oi.target; g += len(gi.b); continue
                raise Mismatch(f"condition differs\n      ours {fmt(oi)}\n      orig {fmt(gi)}")
            # the post-link optimizer inlined the callee: sub esp,4 / callee body / add esp,4+n
            if oi.kind == "call" and gi.b == b"\x83\xec\x04":
                rc = resolve_callee(ctx.obj, ctx.sec, oi)
                if rc is None or _depth + sum(1 for _ in _chain(ctx)) > 3:
                    raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (inlined call: callee unknown)")
                ctx = _Ctx(rc[0], rc[1], dis, ret=(ctx, o + len(oi.b)))
                o = ctx.start; g += 3; continue
            # BBT also inlines callees that take no arguments and no stack without the sub esp,4
            # frame: our 'call f' vs the body of f in place (MATCHING_NOTES 30)
            if oi.kind == "call" and gi.kind not in ("call",) and gi.b != b"\x83\xec\x04":
                rc = resolve_callee(ctx.obj, ctx.sec, oi)
                if rc is not None and _depth + sum(1 for _ in _chain(ctx)) <= 3:
                    ctx = _Ctx(rc[0], rc[1], dis, ret=(ctx, o + len(oi.b))); ctx.bare = True
                    o = ctx.start; continue
            if oi.kind == "ret" and ctx.ret is not None and getattr(ctx, "bare", False):
                if oi.b != b"\xc3":
                    raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (end of frameless inlined call)")
                ctx, o = ctx.ret; continue
            # BBT also folds the callee's own `add esp,a` just before its `ret n` into the single
            # `add esp,a+4+n(+caller's cleanup)` it emits for the inlined call (MATCHING_NOTES 45)
            if ctx.ret is not None and not getattr(ctx, "bare", False) and _add_esp(oi.b) is not None \
                    and _add_esp(gi.b) is not None:
                nxt = ctx.ours.get(o + len(oi.b))
                if nxt is not None and nxt.kind == "ret":
                    a = _add_esp(oi.b)
                    n = 4 + (struct.unpack_from("<H", nxt.b, 1)[0] if nxt.b[0] == 0xC2 else 0)
                    x = _add_esp(gi.b)
                    if x > a and x >= a + n:
                        caller, co = ctx.ret
                        extra = x - a - n
                        if extra:
                            ni = caller.ours.get(co)
                            if ni is None or _add_esp(ni.b) != extra:
                                raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (folded stack cleanup)")
                            co += len(ni.b)
                        g += len(gi.b)
                        ctx, o = caller, co
                        continue
            if oi.kind == "ret" and ctx.ret is not None:
                # end of an inlined callee: the original drops return address + arguments instead
                n = 4 + (struct.unpack_from("<H", oi.b, 1)[0] if oi.b[0] == 0xC2 else 0)
                x = _add_esp(gi.b)
                if x is None or x < n:
                    raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (end of inlined call)")
                caller, co = ctx.ret
                g += len(gi.b); extra = x - n
                if extra:                        # BBT folded the caller's 'add esp,extra' into it
                    ni = caller.ours.get(co)
                    if ni is None or _add_esp(ni.b) != extra:
                        raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)} (stack cleanup after inlined call)")
                    co += len(ni.b)
                ctx, o = caller, co; continue
            # everything else: same length, same bytes except relocated fields
            if len(oi.b) == len(gi.b) + 1 and same_without_disp0(oi, gi, ctx.relmask):
                pass                 # BBT re-encoded [reg+0] as [reg] (MATCHING_NOTES 16)
            elif len(oi.b) != len(gi.b):
                raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)}")
            else:
                for j in range(len(oi.b)):
                    if oi.b[j] != gi.b[j] and (oi.addr + j) not in ctx.relmask:
                        raise Mismatch(f"ours {fmt(oi)}\n      orig {fmt(gi)}")
            if SYMCHECK is not None:
                SYMCHECK(ctx.obj, ctx.sec, oi, gi)
            if oi.kind == "ijmp":
                follow_table(ctx.obj, ctx.sec, oi, gi, orig, work, ctx)
                break
            if oi.kind == "ret":
                break
            o += len(oi.b); g += len(gi.b)
    # our instructions never reached: ignore nop padding and data (index tables) after the code
    reached = [o for (c, o) in visited if c == id(top)]
    reached_end = max(reached) if reached else top.start
    missing = [a for a in top.ours if (id(top), a) not in visited and a < reached_end and top.ours[a].b != b"\x90"]
    if missing: notes.append(f"{len(missing)} of our instructions never reached (jump-table data?)")
    if SYMCHECK is not None and _depth == 0 and SYMCHECK.unverified:
        notes.append(f"{len(SYMCHECK.unverified)} unverified references")
    return covered, "; ".join(notes)

def _chain(ctx):
    while ctx is not None:
        yield ctx
        ctx = ctx.ret[0] if ctx.ret else None

def same_tail(orig, a, b, n=8):
    """Two original blocks that are byte-identical up to a ret (BBT duplicates / merges epilogues)."""
    for _ in range(n):
        x, y = orig.at(a), orig.at(b)
        if x is None or y is None or x.b != y.b or x.kind in ("jmp", "jcc", "call", "icall", "ijmp"):
            return False
        if x.kind == "ret":
            return True
        a += len(x.b); b += len(y.b)
    return False

def same_without_disp0(oi, gi, relmask):
    """True if gi is oi with a zero 8-bit displacement removed: ModRM mod=01 -> mod=00
    ([esp+0] -> [esp], [ecx+0] -> [ecx]; not for an ebp base, which has no short form)."""
    b, g = oi.b, gi.b
    for j in range(len(b) - 1):
        m = b[j]
        if m >> 6 != 1: continue
        rm = m & 7
        k = j + 1                               # position of the disp8
        if rm == 4:                             # SIB follows
            if j + 2 >= len(b) or (b[j + 1] & 7) == 5: continue
            k = j + 2
        elif rm == 5:
            continue
        if k >= len(b) or b[k] != 0: continue
        cand = b[:j] + bytes([m & 0x3F]) + b[j + 1:k] + b[k + 1:]
        if len(cand) != len(g): continue
        ok = True
        for x in range(len(cand)):
            src = x if x < k else x + 1         # position in our bytes
            if cand[x] != g[x] and (oi.addr + src) not in relmask:
                ok = False; break
        if ok: return True
    return False

EXTERN = {}          # name -> (obj, index): functions of other objects, for cross-object BBT inlining

def register_obj(obj):
    for i, f in enumerate(obj.funcs):
        if obj.sections[f[0]]["ch"] & 0x1000 and f[2] in EXTERN:   # COMDAT: keep the first copy
            continue
        EXTERN.setdefault(f[2], (obj, i))

def resolve_callee(obj, sec, oi):
    """(object, function index) our call/jmp at oi goes to: this object first, then EXTERN."""
    rel = obj.sections[sec]["rels"].get(oi.addr + 1)
    if rel is None:
        return None
    name = obj.syms.get(rel[0], (None,))[0]
    k = next((i for i, f in enumerate(obj.funcs) if f[2] == name), None)
    if k is not None:
        return obj, k
    return EXTERN.get(name)

_ENTRIES = None
def function_entries():
    """Function start addresses from Notes/inventory.csv (empty set if it is missing)."""
    global _ENTRIES
    if _ENTRIES is None:
        import csv as _csv
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Notes", "inventory.csv")
        _ENTRIES = {int(r["va"], 16) for r in _csv.DictReader(open(p))} if os.path.exists(p) else set()
    return _ENTRIES

def tail_callee(obj, sec, oi):
    return resolve_callee(obj, sec, oi)

def bbt_inlined_call(obj, sec, oi, g, orig, dis):
    """Our 'call f' vs the original 'sub esp,4; <body of f without ret>; add esp,4+n'.
    f must be defined in our object and be straight-line code. Returns the original address after
    the sequence, or None."""
    rc = resolve_callee(obj, sec, oi)
    if rc is None:
        return None
    cobj, k = rc
    csec, cstart, cend = cobj.func_bytes(k)
    C = cobj.sections[csec]; craw = C["raw"]
    mask = set()
    for va in C["rels"]:
        if cstart <= va < cend:
            mask.update(range(va, va + 4))
    g += 3
    a = cstart
    lens = dis.lengths(craw[cstart:cend], cstart)
    while a in lens:
        ln = lens[a][0]; b = craw[a:a + ln]
        if b[0] in (0xC3, 0xC2):
            n = 4 + (struct.unpack_from("<H", b, 1)[0] if b[0] == 0xC2 else 0)
            gi = orig.at(g)
            if gi is None: return None
            # BBT may fold the caller's own 'add esp,m' into it: add esp,4+n+m (returned as 'extra')
            if len(gi.b) == 3 and gi.b[:2] == b"\x83\xc4" and gi.b[2] >= n: return g + 3, gi.b[2] - n
            if len(gi.b) == 6 and gi.b[:2] == b"\x81\xc4":
                x = struct.unpack_from("<I", gi.b, 2)[0]
                if x >= n: return g + 6, x - n
            return None
        if classify(a, b)[0] not in ("other", "icall", "call"):
            return None
        gi = orig.at(g)
        if gi is None or len(gi.b) != ln:
            return None
        if any(b[j] != gi.b[j] and (a + j) not in mask for j in range(ln)):
            return None
        a += ln; g += ln
    return None

def reloc_target(obj, sec, va, raw):
    """Section offset a DIR32 relocation at 'va' points to, if it is inside section 'sec'."""
    S = obj.sections[sec]
    si, typ = S["rels"][va]
    name, value, secnum, scl = obj.syms.get(si, (None, 0, 0, 0))
    if secnum - 1 != sec:
        return None
    return value + struct.unpack_from("<I", raw, va)[0]

def follow_table(obj, sec, oi, gi, orig, work, ctx=None):
    """jmp dword ptr [reg*4 + table]: pair up our table entries with the original's."""
    S = obj.sections[sec]
    tpos = None
    for j in range(len(oi.b) - 3):
        if (oi.addr + j) in S["rels"]:
            tpos = j
    if tpos is None:
        return
    our_tab = reloc_target(obj, sec, oi.addr + tpos, S["raw"])
    orig_tab = struct.unpack_from("<I", gi.b, tpos)[0]
    if our_tab is None:
        return
    n = 0
    while (our_tab + 4 * n) in S["rels"] and n < 1024:
        tgt = reloc_target(obj, sec, our_tab + 4 * n, S["raw"])
        gt = orig.pe.u32(orig_tab + 4 * n)
        if tgt is None or gt is None or not orig.pe.in_image(gt):
            raise Mismatch(f"jump table entry {n} unreadable")
        work.append((ctx, tgt, gt) if ctx is not None else (tgt, gt)); n += 1

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("objs", nargs="+")
    ap.add_argument("--map", required=True); ap.add_argument("--report")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pe = PE(a.exe); dis = Disasm(); orig = OrigCode(pe, dis)
    enable_symcheck(a.exe, a.map)
    patterns = []
    for ln in open(a.map, errors="replace"):
        ln = ln.split("#", 1)[0].strip()
        if "=" in ln:
            k, v = ln.rsplit("=", 1); v = int(v.strip(), 0)
            patterns.append((k.strip(), v if v >= pe.base else v + pe.base))
    def lookup(name):
        for k, v in patterns:
            if k == name: return v
        for k, v in patterns:
            if k in name: return v
        return None
    paths = [p for pat in a.objs for p in (sorted(glob.glob(pat)) or [pat])]
    res, extras = {}, {}
    objs = {p: Obj(p) for p in paths}
    for o in objs.values():          # callees in other objects (BBT inlining across files)
        register_obj(o)
    for p in paths:
        obj = objs[p]
        for k, (sec, val, name) in enumerate(obj.funcs):
            va = lookup(name)
            if va is None:
                extras[name] = os.path.basename(p); continue
            try:
                cov, note = compare_function(obj, k, va, orig, dis)
                st = "MATCH"; detail = note
                ranges = sorted(cov)
                chunks = []
                for x in ranges:
                    if chunks and x == chunks[-1][1]: chunks[-1][1] = x + 1
                    else: chunks.append([x, x + 1])
                detail = (note + "  " if note else "") + "original blocks: " + \
                         ", ".join(f"{s:#x}-{e:#x}" for s, e in chunks[:8]) + (" ..." if len(chunks) > 8 else "")
            except Mismatch as e:
                st, detail = "MISMATCH", str(e)
            old = res.get(name)
            if old is None or (old[0] != "MATCH" and st == "MATCH"):
                res[name] = (st, va, detail, os.path.basename(p))
    good = {n: r for n, r in res.items() if r[0] == "MATCH"}
    bad = {n: r for n, r in res.items() if r[0] != "MATCH"}
    rep = a.report or os.path.join("reports", "zoo_report.txt")
    os.makedirs(os.path.dirname(rep) or ".", exist_ok=True)
    L = [f"Zoo Tycoon compare report - {datetime.datetime.now():%Y-%m-%d %H:%M}",
         f"target: {a.exe}  map: {a.map} ({len(patterns)} entries)",
         f"objects: {', '.join(os.path.basename(p) for p in paths)}", "",
         f"SUMMARY  matched {len(good)} | mismatched {len(bad)} | not in map {len(extras)}", "",
         f"MISMATCHES ({len(bad)})"]
    for n, (st, va, det, f) in sorted(bad.items(), key=lambda kv: kv[1][1]):
        L += [f"  {va:#x}  {n}   [{f}]", f"      {det}"]
    L += ["", f"MATCHED ({len(good)})"]
    for n, (st, va, det, f) in sorted(good.items(), key=lambda kv: kv[1][1]):
        L += [f"  {va:#x}  {n}"] + ([f"      {det}"] if a.verbose or "never" in det else [])
    L += ["", f"NOT IN MAP ({len(extras)})"] + [f"  {n}   [{f}]" for n, f in sorted(extras.items())]
    open(rep, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"matched {len(good)} | mismatched {len(bad)} | not in map {len(extras)}")
    for n, (st, va, det, f) in sorted(bad.items(), key=lambda kv: kv[1][1])[:12]:
        print(f"  MISMATCH {va:#x} {n}\n      {det}")
    print(f"report: {os.path.abspath(rep)}")
    sys.exit(0 if not bad else 1)

if __name__ == "__main__":
    main()
