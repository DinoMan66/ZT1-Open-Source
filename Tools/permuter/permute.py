#!/usr/bin/env python3
"""
permute.py - background permuter: tries mechanical rewrites of ONE function until the compiler's output is the
original's. No AI and no usage: it runs on the PC, the VM compiles, the project's own comparison scores.
Free tool (Tools\\TOOLS.md). Works in both projects (Zoo Tycoon / JPOG).

    py Tools\\permuter\\permute.py gx\\gxlledither.cpp GXLLE::drawDitherMirror32
    py Tools\\permuter\\permute.py TKernelInterface\\TVector3.cpp TVector3::Normalise --rounds 60 --batch 24
    py Tools\\permuter\\permute.py --list [N]                 near misses in the last build, closest first
    py Tools\\permuter\\permute.py --auto 10 --host           overnight: the 10 closest near misses one after another

  <file>      the source file, relative to Src\\
  <function>  Class::method (or a plain function name) as written in that file; --sym TEXT picks the compiled
              symbol when the name is ambiguous (overloads): any part of the decorated name
  --rounds N  build rounds (default 30)      --batch N  variants per round (default 20)
  --seed N    repeatable run                 --types    also try int / unsigned / long for locals
  --no-rebuild  don't queue a normal full build at the end
  --host      build on this PC (Tools\\hostbuild, set up and --check'ed first): seconds per round, Results\\ untouched
  --auto N    work through the N closest functions of --list unattended (each with --rounds/--batch; a function
              that turns out not to be a near miss is dropped after its first build; functions that already have a
              report are skipped unless --again). Summary: Notes\\permuter\\AUTO_<date>.md. Ctrl+C stops cleanly.
              Notes\\PERMUTER_TARGETS.txt (written by a session: "<folder\\file.cpp> <Class::method> [sym]" per line;
              sym = part of the decorated name, for overloads) is
              run first; afterwards it is moved to Notes\\permuter\\PERMUTER_TARGETS_<date>.done.txt.

What it does, each round: makes N copies of the file with small rewrites inside the function, puts them in a
scratch folder Src\\zzperm\\, asks the VM for a build of that folder only, scores every copy against the original
and keeps the closest as the next starting point. It stops at an exact result or after --rounds.

Rewrites (meaning-preserving spellings a programmer could have written, never added code): swap two neighbouring
statements, reorder local declarations, split or join a declaration and its first assignment, swap the operands
of + * & | ^ == !=, turn a < b into b > a, x++ / ++x / x += 1, x = x + e / x += e, if (x) / if (x != 0),
if (!x) / if (x == 0). It never adds casts, temporaries, pragmas or dead code (READABILITY_STANDARD.md).

Result: Notes\\permuter\\<file>__<function>.md - the score per round and the best rewrites as diffs. An exact
result is a CANDIDATE: put the change into the real file and let a normal build round and the anti-cheat verify
it (this tool does not check call / data targets on JPOG, and never edits Src\\ outside its scratch folder).

Needs: Tools\\watch.bat running in the VM; capstone or objdump as for the other tools. Don't run it while a Claude
session is building or while the anti-cheat runs: Tools\\queue\\permuter.lock exists while it works, and Results\\
holds permuter builds until its final full build (or run the anti-cheat with --rebuild).
Ideas from decomp-permuter (simonlindholm) and decompdecomp's simple rewrites.
"""
import argparse, csv, datetime, difflib, glob, hashlib, importlib.util, os, random, re, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(ROOT, "Tools")
SCRATCH = "zzperm"
RESULTS = os.path.join(ROOT, "Results")     # Results_host with --host (Tools\hostbuild)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))

# ---------------------------------------------------------------------------------------------- the source side
_KEYWORDS = {"if", "for", "while", "switch", "catch", "return", "sizeof", "do", "else"}


def strip_code(t):
    """comments and string contents blanked, same length and line breaks"""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    t = re.sub(r"/\*.*?\*/", blank, t, flags=re.S)
    t = re.sub(r"//[^\n]*", blank, t)
    return re.sub(r'"(\\.|[^"\\\n])*"', lambda m: '"' + " " * (len(m.group(0)) - 2) + '"', t)


def _inside_body(code, pos):
    """True when pos is inside braces other than namespace / extern "C" blocks"""
    stack = []
    for m in re.finditer(r"[{}]", code[:pos]):
        if m.group(0) == "{":
            head = code[max(0, m.start() - 120):m.start()]
            stack.append(bool(re.search(r"(\bnamespace\s+\w*|extern\s*\"\s*C?\s*\")\s*$", head)))
        elif stack:
            stack.pop()
    return any(not ns for ns in stack)


def find_function(text, name):
    """-> (index of '{', index of matching '}') of the definition of `name` (Class::method or plain)"""
    code = strip_code(text)
    pat = re.compile(r"(?<![\w:])" + re.escape(name).replace(r"\:\:", r"\s*::\s*") + r"\s*\(")
    for m in pat.finditer(code):
        i, depth = m.end() - 1, 0
        while i < len(code):                        # closing parenthesis of the parameter list
            if code[i] == "(": depth += 1
            elif code[i] == ")":
                depth -= 1
                if depth == 0: break
            i += 1
        j = i + 1
        while j < len(code) and code[j] not in "{;":      # const, initialiser list ...
            j += 1
        if j >= len(code) or code[j] != "{":
            continue                                # a declaration or a call
        if _inside_body(code, m.start()):
            continue                                # inside another function or class body: a call
        depth, k = 0, j
        while k < len(code):
            if code[k] == "{": depth += 1
            elif code[k] == "}":
                depth -= 1
                if depth == 0:
                    return j, k
            k += 1
    return None


_TYPE = r"(?:const\s+)?(?:unsigned\s+|signed\s+)?[A-Za-z_]\w*(?:\s*::\s*\w+)*(?:\s*<[^;<>]*>)?"
_DECL = re.compile(r"^(\s+)(" + _TYPE + r")(\s*[\*&]*\s+[\*&]*\s*|\s*[\*&]+\s*)([A-Za-z_]\w*)(\s*=\s*([^;]+))?;\s*$")
_STMT = re.compile(r"^\s+[^\s{}#/][^{}]*;\s*$")
_CONTROL = re.compile(r"\b(return|break|continue|goto|case|default|delete|throw)\b|^\s*(else|for|while|do|switch|if)\b")
_NOT_TYPE = {"return", "delete", "goto", "else", "case", "throw", "new", "break", "continue", "typedef", "using"}
_OPND = r"[A-Za-z_][\w]*(?:(?:->|\.)\w+|\[[^\[\]]*\])*|\d+|0x[0-9a-fA-F]+"


def indent(l): return l[:len(l) - len(l.lstrip())]
def is_decl(l):
    m = _DECL.match(l)
    return m if m and m.group(2).split()[-1] not in _NOT_TYPE and m.group(2) not in _NOT_TYPE else None
def code_part(l): return l.split("//")[0].rstrip()
def tail(l): return l[len(code_part(l)):]


def m_swap_statements(L, rng, opt):
    c = [i for i in range(len(L) - 1) if _STMT.match(code_part(L[i])) and _STMT.match(code_part(L[i + 1]))
         and not _CONTROL.search(code_part(L[i])) and not _CONTROL.search(code_part(L[i + 1]))
         and not is_decl(code_part(L[i])) and not is_decl(code_part(L[i + 1])) and indent(L[i]) == indent(L[i + 1])]
    if not c: return None
    i = rng.choice(c); L[i], L[i + 1] = L[i + 1], L[i]; return "swap statements"


def m_move_declaration(L, rng, opt):
    c = [i for i in range(len(L) - 1) if is_decl(code_part(L[i])) and is_decl(code_part(L[i + 1]))
         and indent(L[i]) == indent(L[i + 1])]
    if not c: return None
    i = rng.choice(c); L[i], L[i + 1] = L[i + 1], L[i]; return "reorder declarations"


def m_split_or_join(L, rng, opt):
    split = [i for i in range(len(L)) if (lambda m: m and m.group(5) and "&" not in m.group(3)
                                           and not m.group(2).startswith("const"))(is_decl(code_part(L[i])))]
    join = []
    for i in range(len(L) - 1):
        m = is_decl(code_part(L[i]))
        if m and not m.group(5):
            a = re.match(r"^\s+" + re.escape(m.group(4)) + r"\s*=\s*([^;=][^;]*);\s*$", code_part(L[i + 1]))
            if a: join.append((i, m, a))
    pick = rng.choice(["split"] * len(split) + ["join"] * len(join)) if split or join else None
    if pick == "split":
        i = rng.choice(split); m = is_decl(code_part(L[i]))
        L[i:i + 1] = [f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)};{tail(L[i])}",
                      f"{m.group(1)}{m.group(4)} = {m.group(6).strip()};"]
        return "split declaration and assignment"
    if pick == "join":
        i, m, a = rng.choice(join)
        L[i:i + 2] = [f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)} = {a.group(1).strip()};{tail(L[i])}"]
        return "join declaration and assignment"
    return None


_BEFORE_OK = re.compile(r"(?:^|[(=,;?:\[{]|&&|\|\||[<>!=]=|[<>]|\breturn)\s*$")
_AFTER_OK = re.compile(r"^\s*(?:$|[),;?:\]]|&&|\|\||[<>!=]=|[<>](?![<>]))")
def _whole_operands(line, m):
    """the match is a complete sub-expression: nothing binds tighter on either side (a - b + c is not b + c)"""
    return bool(_BEFORE_OK.search(line[:m.start()]) and _AFTER_OK.match(line[m.end():]))


def _rewrite_line(L, rng, rx, repl, what, whole=False):
    c = [(i, m) for i in range(len(L)) for m in rx.finditer(code_part(L[i]))
         if not whole or _whole_operands(code_part(L[i]), m)]
    if not c: return None
    i, m = rng.choice(c)
    body = code_part(L[i])
    new = repl(m)
    if new is None: return None
    L[i] = body[:m.start()] + new + body[m.end():] + tail(L[i])
    return what


_COMMUTE = re.compile(r"(?<![\w.>\]])(" + _OPND + r") (\+|\*|&|\||\^|==|!=) (" + _OPND + r")(?![\w\[(.]|->)")
def m_commute(L, rng, opt):
    return _rewrite_line(L, rng, _COMMUTE, lambda m: f"{m.group(3)} {m.group(2)} {m.group(1)}", "swap operands", whole=True)


_COMPARE = re.compile(r"(?<![\w.>\]])(" + _OPND + r") (<=|>=|<|>) (" + _OPND + r")(?![\w\[(.]|->)")
_FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}
def m_flip_compare(L, rng, opt):
    return _rewrite_line(L, rng, _COMPARE, lambda m: f"{m.group(3)} {_FLIP[m.group(2)]} {m.group(1)}", "turn a comparison round", whole=True)


_INC = re.compile(r"^(\s+)(?:(" + _OPND + r")(\+\+|--)|(\+\+|--)(" + _OPND + r")|(" + _OPND + r") (\+|-)= 1);\s*$")
def m_incdec(L, rng, opt):
    c = [i for i in range(len(L)) if _INC.match(code_part(L[i]))]
    if not c: return None
    i = rng.choice(c); m = _INC.match(code_part(L[i]))
    var = m.group(2) or m.group(5) or m.group(6)
    op = m.group(3) or m.group(4) or (m.group(7) * 2)
    forms = [f"{var}{op};", f"{op}{var};", f"{var} {op[0]}= 1;"]
    cur = code_part(L[i]).strip()
    L[i] = m.group(1) + rng.choice([f for f in forms if f != cur]) + tail(L[i])
    return "increment spelling"


_COMPOUND = re.compile(r"^(\s+)(" + _OPND + r") = \2 (\+|-|\*|&|\||\^) ([^;]+);\s*$")
_COMPOUND2 = re.compile(r"^(\s+)(" + _OPND + r") (\+|-|\*|&|\||\^)= ([^;]+);\s*$")
def m_compound(L, rng, opt):
    c = [i for i in range(len(L)) if _COMPOUND.match(code_part(L[i])) or _COMPOUND2.match(code_part(L[i]))]
    if not c: return None
    i = rng.choice(c); body = code_part(L[i])
    m = _COMPOUND.match(body)
    if m:
        L[i] = f"{m.group(1)}{m.group(2)} {m.group(3)}= {m.group(4).strip()};{tail(L[i])}"
    else:
        m = _COMPOUND2.match(body)
        rhs = m.group(4).strip()
        if re.search(r"[-+*/%&|^<>?:=]", rhs): rhs = f"({rhs})"
        L[i] = f"{m.group(1)}{m.group(2)} = {m.group(2)} {m.group(3)} {rhs};{tail(L[i])}"
    return "x = x op e  <->  x op= e"


_TRUTH = re.compile(r"\b(if|while) \((!?)(" + _OPND + r")( [!=]= 0)?\)")
def m_truth(L, rng, opt):
    def repl(m):
        kw, neg, x, cmp0 = m.groups()
        if cmp0 and neg: return None
        if cmp0:   return f"{kw} ({'!' if cmp0.strip() == '== 0' else ''}{x})"
        return f"{kw} ({x} {'==' if neg else '!='} 0)"
    return _rewrite_line(L, rng, _TRUTH, repl, "if (x)  <->  if (x != 0)")


_INTS = ["int", "unsigned int", "long", "unsigned long"]
def m_retype(L, rng, opt):
    if not opt.types: return None
    c = [i for i in range(len(L)) if (lambda m: m and m.group(2) in _INTS)(is_decl(code_part(L[i])))]
    if not c: return None
    i = rng.choice(c); m = is_decl(code_part(L[i]))
    new = rng.choice([t for t in _INTS if t != m.group(2)])
    body = code_part(L[i])
    L[i] = body[:m.start(2)] + new + body[m.end(2):] + tail(L[i])
    return f"local type {m.group(2)} -> {new} (review: is it plausible?)"


MUTATIONS = [(m_swap_statements, 5), (m_move_declaration, 5), (m_split_or_join, 3), (m_commute, 5),
             (m_flip_compare, 3), (m_incdec, 2), (m_compound, 3), (m_truth, 2), (m_retype, 2)]


def mutate(body, rng, opt):
    """-> (new body, [what was done]) or None"""
    L = body.split("\n")
    done = []
    for _ in range(rng.choice([1, 1, 1, 2, 2, 3])):
        for _try in range(8):
            f = rng.choices([m for m, _ in MUTATIONS], weights=[w for _, w in MUTATIONS])[0]
            what = f(L, rng, opt)
            if what:
                done.append(what); break
    new = "\n".join(L)
    return (new, done) if done and new != body else None


# ---------------------------------------------------------------------------------------------- the scoring side
def load_tools():
    import inspect, dis                             # the standard 'dis' first: Zoo has a Tools\dis.py of its own
    try: import capstone                            # noqa: F401
    except Exception: pass
    sys.path.insert(0, TOOLS)
    import compare as C
    return C


def symbol_pattern(function, sym):
    if sym: return sym
    if "::" in function:
        cls, meth = function.rsplit("::", 1)
        cls = cls.split("::")[-1]
        if meth == cls: return f"??0{cls}@"
        if meth == "~" + cls: return f"??1{cls}@"
        return f"?{meth}@{cls}@"
    return f"?{function}@@"


class ZooScore:
    def __init__(self, pattern):
        self.C = C = load_tools()
        spec = importlib.util.spec_from_file_location("zoo_dis", os.path.join(TOOLS, "dis.py"))
        self.D = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.D)
        exe = os.path.join(ROOT, "Original", "zoo.exe"); mp = os.path.join(ROOT, "Notes", "zoo.map")
        self.pe = C.PE(exe); self.dis = C.Disasm(); self.orig = C.OrigCode(self.pe, self.dis)
        C.enable_symcheck(exe, mp)
        self.pattern = pattern
        self.map = []
        for ln in open(mp, errors="replace"):
            ln = ln.split("#", 1)[0].strip()
            if "=" in ln:
                k, v = ln.rsplit("=", 1); v = int(v.strip(), 0)
                self.map.append((k.strip(), v if v >= self.pe.base else v + self.pe.base))
        for p in glob.glob(os.path.join(TOOLS, "lib", "*.obj")):
            try: C.register_obj(C.Obj(p))
            except Exception: pass
        self.oseq = None

    def _va(self, name):
        for k, v in self.map:
            if k == name: return v
        for k, v in self.map:
            if k in name: return v

    @staticmethod
    def _norm(t):
        t = re.sub(r"0x[0-9a-f]+", "N", t.lower())
        return re.sub(r"\s+", " ", re.sub(r"\b\d+\b", "N", t)).strip()

    def score(self, stem):
        """-> (distance 0..1, exact) for Results\\zzperm.<stem>.obj, None when it did not compile"""
        p = os.path.join(RESULTS, f"{SCRATCH}.{stem}.obj")
        if not os.path.exists(p): return None
        C = self.C
        obj = C.Obj(p); C.register_obj(obj)
        ks = [i for i, f in enumerate(obj.funcs) if self.pattern in f[2]]
        if not ks: raise SystemExit(f"no compiled function matches '{self.pattern}' - use --sym (functions: "
                                    + ", ".join(f[2] for f in obj.funcs[:12]) + " ...)")
        if len({obj.funcs[i][2] for i in ks}) > 1:
            raise SystemExit("several functions match: use --sym with more of the decorated name: "
                             + ", ".join(sorted({obj.funcs[i][2] for i in ks})))
        k = ks[0]; va = self._va(obj.funcs[k][2])
        if va is None: raise SystemExit(f"{obj.funcs[k][2]} is not in Notes\\zoo.map")
        if self.oseq is None:
            seen, _ = self.D.blocks(self.orig, va)
            self.oseq = [self._norm(seen[x].text) for x in sorted(seen, key=lambda x: (x < va, x))]
        sec, s, e = obj.func_bytes(k)
        raw = obj.sections[sec]["raw"]
        seq = [self._norm(t) for a, (ln, t) in sorted(self.dis.lengths(raw[s:e], s).items()) if raw[a:a + ln] != b"\x90"]
        dist = 1.0 - difflib.SequenceMatcher(None, self.oseq, seq, autojunk=False).ratio()
        try:
            C.compare_function(obj, k, va, self.orig, self.dis); exact = True
        except C.Mismatch:
            exact = False
        except Exception:
            exact = False
        return (0.0 if exact else max(dist, 1e-6)), exact


class JpogScore:
    def __init__(self, pattern, folder):
        self.C = C = load_tools()
        self.pattern = pattern
        cands = glob.glob(os.path.join(ROOT, "Original", "**", folder + "*.dll"), recursive=True) + \
                glob.glob(os.path.join(ROOT, "Original", folder + "*.exe"))
        if not cands: raise SystemExit(f"no original binary for Src\\{folder} under Original\\")
        dll = sorted(cands, key=lambda p: ("_inst" not in p, len(p)))[0]
        self.d, self.r2o, self.exports, _ = C.load_dll(dll)
        self.map = {}
        mp = os.path.join(ROOT, "Notes", folder + ".map")
        if os.path.exists(mp):
            for ln in open(mp, errors="replace"):
                ln = ln.split("#")[0].strip()
                if "=" in ln:
                    k, v = ln.split("=", 1); self.map[k.strip()] = int(v.strip(), 16)

    def score(self, stem):
        """-> (differing bytes, exact) for Results\\zzperm.<stem>.txt, None when it did not compile"""
        p = os.path.join(RESULTS, f"{SCRATCH}.{stem}.txt")
        if not os.path.exists(p): return None
        C = self.C
        rel = C.obj_relocs(p[:-4] + ".obj")
        funcs = {n: ins for n, ins in C.parse_dumpbin(p).items() if ins and self.pattern in n}
        if not funcs: raise SystemExit(f"no compiled function matches '{self.pattern}' - use --sym")
        if len(funcs) > 1:
            raise SystemExit("several functions match: use --sym with more of the decorated name: " + ", ".join(sorted(funcs)))
        name, ins = next(iter(funcs.items()))
        rva = self.exports.get(name)
        if rva is None:
            rva = next((v for k, v in self.map.items() if k in name), None)
        if rva is None: raise SystemExit(f"{name}: not an export and not in the DLL's .map")
        status, ours, theirs, first = C.compare(name, ins, self.d, self.r2o(rva), rel.get(name))
        if status.startswith("MATCH"):
            return 0, True
        # bytes that have no counterpart when the two are aligned (a plain position-by-position count would
        # call everything after one inserted instruction different); relocated fields are masked in ours
        tol = set()
        for r in rel.get(name, ()): tol.update(range(r, r + 4))
        a = bytes(0 if i in tol else x for i, x in enumerate(bytes(ours)))
        b = bytes(theirs)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        same = sum(blk.size for blk in sm.get_matching_blocks())
        return max(max(len(a), len(b)) - same, 1), False


# ---------------------------------------------------------------------------------------------- the build loop
def request_build(ident, folder):
    q = os.path.join(TOOLS, "queue"); os.makedirs(q, exist_ok=True)
    line = f"{ident} {int(time.time())}" + (f" {folder}" if folder else (" all" if ZOO else ""))
    name = f"request_{ident}.txt" if ZOO else "request.txt"
    with open(os.path.join(q, name), "w", newline="") as f:
        f.write(line + "\r\n")


def wait_done(ident, timeout):
    done = os.path.join(ROOT, "Results", "DONE.txt")
    t0 = time.time()
    while time.time() - t0 < timeout:
        try: txt = open(done, errors="replace").read().strip()
        except OSError: txt = ""
        if txt.startswith(ident + " "):
            return txt.endswith("OK")
        time.sleep(2)
    raise SystemExit("the VM did not answer - is Tools\\watch.bat running there?")


def list_candidates(resdir, limit):
    """near misses in the last build, closest first (Tools/batch.py does the judging)"""
    spec = importlib.util.spec_from_file_location("batch_tool", os.path.join(TOOLS, "batch.py"))
    B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
    pat = "*.obj" if ZOO else "*.txt"
    files = sorted({tuple(os.path.basename(p).split(".")[:2]) for p in glob.glob(os.path.join(resdir, pat))
                    if os.path.basename(p).count(".") >= 2 and not os.path.basename(p).endswith(".compile.txt")
                    and not os.path.basename(p).split(".")[1].startswith(("Var", "p0", "p1", "p2"))
                    and os.path.basename(p).split(".")[0] != SCRATCH})
    judge = B.judge_zoo if ZOO else B.judge_jpog
    best, matched = {}, set()
    for folder, stem in files:                    # one file at a time, to know where each function is written
        for st, size, note, what in judge([(folder, stem)], resdir):
            if st == "MATCH":
                matched.add(what)
            elif st == "DIFF":
                m = re.search(r"(\d+) bytes differ", note)
                n = int(m.group(1)) if m else 10**6
                if what not in best or n < best[what][0]:
                    best[what] = (n, size, what, note, f"{folder}\\{stem}.cpp")
    near = [v for w, v in best.items() if w not in matched]   # an inline that matches in another file counts
    near.sort()
    if limit is None:
        return near
    print(f"written but not matching, closest first ({'bytes that differ' if not ZOO else 'Zoo: no byte count - all listed'}):")
    for n, size, what, note, src in near[:limit]:
        print(f"  {'' if n == 10**6 else n:>5}  of {size:>5}  {what[:58]:58}  {src}")
    print(f"{len(near)} functions differ. The permuter suits the ones a few bytes away (a register or an order), "
          "not structural differences of dozens of bytes.")


def auto(a):
    """--auto N: the permuter on the closest near misses, one after another (each run is a child process)"""
    import json, subprocess
    resdir = os.path.join(ROOT, "Results")
    notes = os.path.join(ROOT, "Notes", "permuter"); os.makedirs(notes, exist_ok=True)
    picked = []
    # 1. the session's own choice: Notes\PERMUTER_TARGETS.txt, one "<folder\file.cpp> <Class::method>" per line
    tfile = os.path.join(ROOT, "Notes", "PERMUTER_TARGETS.txt")
    if os.path.exists(tfile):
        for ln in open(tfile, encoding="utf-8", errors="replace"):
            ln = ln.split("#", 1)[0].strip()
            if not ln: continue
            parts = ln.split()
            if len(parts) not in (2, 3):
                print(f"  PERMUTER_TARGETS.txt: skipped '{ln}' (want: <folder\\file.cpp> <Class::method>)"); continue
            rel = parts[0].replace("/", os.sep).replace("\\", os.sep)
            if rel.lower().startswith("src" + os.sep): rel = rel[4:]
            func = parts[1].strip(); sym = parts[2] if len(parts) == 3 else None   # 3rd: --sym for overloads
            if not os.path.isfile(os.path.join(ROOT, "Src", rel)):
                print(f"  PERMUTER_TARGETS.txt: no such file Src\\{rel}"); continue
            picked.append((10**6, func, rel, re.sub(r"[^\w.-]+", "_", f"{rel}__{func}" + (f"__{sym}" if sym else "")), sym))
            if len(picked) >= a.auto: break
        print(f"{len(picked)} targets from Notes\\PERMUTER_TARGETS.txt")
    # 2. the rest from the last build's near misses (JPOG: closest first; Zoo has no byte count, so order is rough)
    near = list_candidates(resdir, None) if len(picked) < a.auto else []
    for n, size, what, note, src in near:
        func = what.split("  ")[0].strip()
        rel = src.replace("/", os.sep).replace("\\", os.sep)
        if "operator" in func or "`" in func or "::" not in func and not re.match(r"^\w+$", func):
            continue                                            # spellings find_function cannot locate
        tag = re.sub(r"[^\w.-]+", "_", f"{rel}__{func}")
        if os.path.exists(os.path.join(notes, tag + ".md")) and not a.again or any(p[3] == tag for p in picked):
            continue
        picked.append((n, func, rel, tag, None))
        if len(picked) >= a.auto: break
    if not picked:
        print("nothing to do: no near misses without a report (use --again to redo them)"); return
    stamp = f"{datetime.datetime.now():%Y-%m-%d_%H%M}"
    summary = os.path.join(notes, f"AUTO_{stamp}.md")
    lines = [f"# Permuter overnight run {stamp}", "",
             f"{len(picked)} functions, {a.rounds} rounds x {a.batch} variants each, {'host builds' if a.host else 'VM builds'}. "
             "EXACT = a candidate: apply its diff from the function's report, then build and verify normally.", "",
             "| Function | File | Start | Best | Result | Report |", "|---|---|---|---|---|---|"]
    def write():
        with open(summary, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(lines) + "\n")
    write()
    print(f"{len(picked)} functions queued; summary: Notes\\permuter\\{os.path.basename(summary)}")
    try:
        for i, (n, func, rel, tag, sym) in enumerate(picked):
            print(f"\n=== {i + 1}/{len(picked)}  {func}  ({rel}{'' if n == 10**6 else f', {n} bytes differ'})", flush=True)
            cmd = [sys.executable, os.path.abspath(__file__), rel, func, "--rounds", str(a.rounds), "--batch", str(a.batch),
                   "--timeout", str(a.timeout), "--no-rebuild", "--skip-far"] + (["--host"] if a.host else []) + \
                  (["--types"] if a.types else []) + (["--seed", str(a.seed)] if a.seed is not None else []) + \
                  (["--sym", sym] if sym else [])
            res = {}
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
            for ln in p.stdout:
                if ln.startswith("RESULT "):
                    try: res = json.loads(ln[7:])
                    except ValueError: pass
                else:
                    print("   " + ln.rstrip(), flush=True)
            p.wait()
            if not res:
                lines.append(f"| {func} | {rel} | - | - | failed (exit {p.returncode}) | - |")
            else:
                result = "**EXACT**" if res.get("best") == 0 and res.get("changed") else \
                         "already matches" if res.get("best") == 0 else \
                         "dropped: not a near miss" if res.get("far") else \
                         "improved" if res.get("best") is not None and res.get("start") is not None and res["best"] < res["start"] else "no gain"
                fmt = lambda v: "-" if v is None else f"{v:.4g}"
                lines.append(f"| {func} | {rel} | {fmt(res.get('start'))} | {fmt(res.get('best'))} | {result} | {tag}.md |")
            write()
    except KeyboardInterrupt:
        lines.append("\nStopped by Ctrl+C."); write(); print("\nstopped")
    finally:
        if os.path.exists(tfile):                              # done: keep it with the summary, so it is not run again
            try: os.replace(tfile, os.path.join(notes, f"PERMUTER_TARGETS_{stamp}.done.txt"))
            except OSError: pass
        if not a.no_rebuild and not a.host:
            request_build("perm-auto-full", "")
            print("queued a normal full build so Results\\ is back to the real sources")
        print(f"summary: Notes\\permuter\\{os.path.basename(summary)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?"); ap.add_argument("function", nargs="?")
    ap.add_argument("--sym"); ap.add_argument("--rounds", type=int, default=30); ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--seed", type=int); ap.add_argument("--types", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true"); ap.add_argument("--list", nargs="?", const=40, type=int, metavar="N")
    ap.add_argument("--timeout", type=int, default=1200, help="seconds to wait for one build")
    ap.add_argument("--host", action="store_true", help="build on this PC with Tools\\hostbuild (fast, parallel) instead of the VM")
    ap.add_argument("--auto", type=int, metavar="N", help="overnight: the N closest near misses, one after another")
    ap.add_argument("--again", action="store_true", help="--auto: also redo functions that already have a report")
    ap.add_argument("--skip-far", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.auto:
        auto(a); return
    if a.list:
        list_candidates(os.path.join(ROOT, "Results"), a.list); return
    if not a.file or not a.function:
        sys.exit(__doc__)
    rel = a.file.replace("/", os.sep).replace("\\", os.sep)
    src = os.path.join(ROOT, "Src", rel)
    if not os.path.isfile(src): sys.exit(f"no such file: {src}")
    folder = rel.split(os.sep)[0]
    text = open(src, encoding="latin1", newline="").read()
    span = find_function(text, a.function)
    if not span: sys.exit(f"no definition of {a.function} in {rel}")
    b, e = span
    base_body = text[b + 1:e].replace("\r\n", "\n")
    nl = "\r\n" if "\r\n" in text else "\n"
    rng = random.Random(a.seed)
    HB = cfg = None
    if a.host:
        global RESULTS
        spec = importlib.util.spec_from_file_location("hostbuild", os.path.join(TOOLS, "hostbuild", "hostbuild.py"))
        HB = importlib.util.module_from_spec(spec); spec.loader.exec_module(HB)
        cfg = HB.load_config()
        RESULTS = HB.OUT
    scorer = ZooScore(symbol_pattern(a.function, a.sym)) if ZOO else JpogScore(symbol_pattern(a.function, a.sym), folder)
    lock = os.path.join(TOOLS, "queue", "permuter.lock")
    scratch = os.path.join(ROOT, "Src", SCRATCH)
    if os.path.exists(lock): sys.exit("Tools\\queue\\permuter.lock exists: another permuter is running (delete it if not)")
    os.makedirs(os.path.dirname(lock), exist_ok=True); open(lock, "w").write(f"{rel} {a.function} {datetime.datetime.now()}\n")
    notes = os.path.join(ROOT, "Notes", "permuter"); os.makedirs(notes, exist_ok=True)
    tag = re.sub(r"[^\w.-]+", "_", f"{rel}__{a.function}")
    log = [f"# Permuter: {a.function} in Src\\{rel}", "",
           f"Started {datetime.datetime.now():%Y-%m-%d %H:%M}, seed {a.seed}, {a.rounds} rounds x {a.batch} variants. "
           f"Score: {'1 - similarity of the instruction sequences' if ZOO else 'bytes without a counterpart in the original'} (0 = exact). "
           "An exact result is a candidate until a normal build round verifies it.", ""]
    seen = {hashlib.sha1(base_body.encode()).hexdigest()}
    best = (None, base_body, ["(the file as it is)"])           # score, body, history
    results = []                                                # (score, body, history)
    tried = failed = 0
    start_score, far_stop = None, False
    run = "perm%d" % (int(time.time()) % 100000000)
    try:
        for rnd in range(a.rounds + 1):
            shutil.rmtree(scratch, ignore_errors=True); os.makedirs(scratch)
            srcdir = os.path.dirname(src)
            for extra in glob.glob(os.path.join(srcdir, "*.h")) + glob.glob(os.path.join(srcdir, "*.inl")) + \
                         [os.path.join(srcdir, "flags.txt"), src + ".flags"]:
                if os.path.isfile(extra):
                    dst = os.path.basename(extra)
                    shutil.copy2(extra, os.path.join(scratch, dst))
            variants = {}
            if rnd == 0:
                variants["p000_00"] = (base_body, ["(the file as it is)"])
            else:
                guard = 0
                while len(variants) < a.batch and guard < a.batch * 30:
                    guard += 1
                    start_body, hist = (best[1], best[2]) if rng.random() < 0.6 else (base_body, [])
                    r = mutate(start_body, rng, a)
                    if not r: continue
                    body, what = r
                    h = hashlib.sha1(body.encode()).hexdigest()
                    if h in seen: continue
                    seen.add(h)
                    variants[f"p{rnd:03d}_{len(variants):02d}"] = (body, [x for x in hist if not x.startswith("(")] + what)
                if not variants:
                    log.append(f"Round {rnd}: no new rewrites left - stopped."); break
            for stem, (body, _) in variants.items():
                out = text[:b + 1] + body.replace("\n", nl) + text[e:]
                with open(os.path.join(scratch, stem + ".cpp"), "w", encoding="latin1", newline="") as f:
                    f.write(out)
                if os.path.isfile(src + ".flags"):
                    shutil.copy2(src + ".flags", os.path.join(scratch, stem + ".cpp.flags"))
            if HB:
                HB.build(SCRATCH, cfg, quiet=True)
            else:
                ident = f"{run}-{rnd:03d}"
                request_build(ident, SCRATCH)
                wait_done(ident, a.timeout)
                time.sleep(1.5)                                  # the shared folder needs a moment
            round_best = None
            for stem, (body, hist) in variants.items():
                s = scorer.score(stem)
                tried += 1
                if s is None:
                    failed += 1; continue
                results.append((s[0], body, hist))
                if round_best is None or s[0] < round_best[0]: round_best = (s[0], body, hist)
            if rnd == 0:
                if round_best is None: raise SystemExit("the unchanged file did not compile in the scratch folder - see Results\\zzperm.p000_00.compile.txt")
                best = round_best
                print(f"start: score {best[0]:.4g}")
                far = best[0] > (0.08 if ZOO else 24)
                if far:
                    print(f"  note: {best[0]:.4g} is not a near miss - mechanical rewrites rarely close a gap this large "
                          "(it is usually a missing piece of source or a different structure). See --list for closer ones.")
                    log.append("Note: not a near miss at the start; rewrites rarely close a gap this large.")
                    if a.skip_far:
                        start_score = best[0]; far_stop = True
                        log.append("Dropped (overnight run): not a near miss."); break
                log.append(f"Start (unchanged file): score {best[0]:.4g}")
                start_score = best[0]
                if best[0] == 0:
                    print("the function already matches - nothing to do"); break
                continue
            if round_best and round_best[0] < best[0]:
                best = round_best
            line = (f"round {rnd:3d}: {len(variants)} variants, best of round "
                    f"{'-' if round_best is None else '%.4g' % round_best[0]}, best so far {best[0]:.4g}")
            print(line); log.append("- " + line)
            if best[0] == 0:
                print("EXACT: " + "; ".join(best[2])); break
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        try: os.remove(lock)
        except OSError: pass
        results.sort(key=lambda r: r[0])
        top, bodies = [], set()
        for s, body, hist in results:
            if body not in bodies and body != base_body:
                bodies.add(body); top.append((s, body, hist))
            if len(top) == 5: break
        log += ["", f"Tried {tried} variants ({failed} did not compile). Best score {best[0] if best[0] is not None else '-'}.", ""]
        if best[0] == 0 and best[1] != base_body:
            log += ["## EXACT candidate", "", "Apply this change to the real file, then build and verify normally.", ""]
        for s, body, hist in top:
            log += [f"### score {s:.4g}: " + "; ".join(hist), "", "```diff"]
            log += list(difflib.unified_diff(base_body.split("\n"), body.split("\n"), "current", "variant", lineterm="", n=2))
            log += ["```", ""]
        with open(os.path.join(notes, tag + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(log) + "\n")
        print(f"report: Notes\\permuter\\{tag}.md")
        import json
        print("RESULT " + json.dumps({"start": start_score, "best": best[0], "far": far_stop,
                                      "changed": best[1] != base_body, "report": tag + ".md"}), flush=True)
        if not a.no_rebuild and not HB:
            request_build(f"{run}-full", "")
            print("queued a normal full build so Results\\ is back to the real sources")


if __name__ == "__main__":
    main()
