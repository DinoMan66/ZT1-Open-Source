"""genshapes.py - placeholder C++ for small forwarding functions of zoo.exe (Tools/gentrivial.py's big brother).

Recognises a few dozen short shapes that the game repeats with different constants (look up a UI element by
id and call one of its virtual functions, forward to a member object, call a free function with a constant,
...) and writes one placeholder function per address to Src/misc/shapes_unowned.cpp. Names carry the address
(Z_<VA>), so after a build:

    python3 -I Tools/genshapes.py --check Results/misc.shapes_unowned.obj

compares every generated function with the original, appends the matching ones to Notes/zoo.map and stores
the addresses that did not match in Notes/generated/shapes_failed.txt (they are skipped on the next run).
Classes/members are placeholders: Z_<VA>_I is "the interface whose slot N is called", g_<addr> a global.
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trivial as TR, triage_lib as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Src", "misc", "shapes_unowned.cpp")
FAILED = os.path.join(ROOT, "Notes", "generated", "shapes_failed.txt")
H = r"0x([0-9a-f]+)"

def iface(name, slot, ret="void", args=""):
    pads = "".join(f" virtual void p{i}();" for i in range(slot))
    return f"struct {name} {{{pads} virtual {ret} f({args}); }};"

def argl(n, first=0):
    return ", ".join(f"int a{i}" for i in range(first, first + n))

TEXT_END = 0x62C824        # end of .text (0x401000 + 0x22B824)
def cval(v, decls):
    """C++ expression for a pushed constant: addresses become &symbol (keeps the relocation)."""
    if 0x401000 <= v < TEXT_END:
        decls.add(f"void fn_{v:x}();"); return f"(int)&fn_{v:x}"
    if TEXT_END <= v < 0x700000:
        decls.add(f"extern char g_{v:x};"); return f"(int)&g_{v:x}"
    return f"{v:#x}"

def gen(va, s):
    """s = normalised instructions joined with ' ; '. Returns C++ or None."""
    Z = f"Z_{va:X}"; I = Z + "_I"
    def m(p): return re.fullmatch(p, s)
    # 1. element = g.find(id); if (element) element->slot();
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; jmp dword \[edx\+{H}\] ; ret")
    if r:
        idv, g, slot = int(r[1], 16), int(r[2], 16), int(r[5], 16) // 4
        return (f"{iface(I, slot)}\nstruct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}() {{ {I}* e = g_{g:x}_{va:x}.find({idv:#x}); if (e) e->f(); }}")
    # 1b. same with a flag test on the element
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; test byte \[eax\+{H}\],{H} ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; jmp dword \[edx\+{H}\] ; ret")
    if r:
        idv, g, off, mask, slot = int(r[1], 16), int(r[2], 16), int(r[5], 16), int(r[6], 16), int(r[8], 16) // 4
        return (f"struct {I} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void f(); char pad[{off - 4:#x}]; unsigned char flags; }};\n"
                f"struct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}() {{ {I}* e = g_{g:x}_{va:x}.find({idv:#x}); if (e && (e->flags & {mask:#x})) e->f(); }}")
    # 1c. element = g.find(id); if (element) element->method(k);
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; push {H} ; mov ecx,eax ; call {H} ; ret")
    if r:
        idv, g, k = int(r[1], 16), int(r[2], 16), int(r[5], 16)
        return (f"struct {I} {{ void f(int k); }};\nstruct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}() {{ {I}* e = g_{g:x}_{va:x}.find({idv:#x}); if (e) e->f({k:#x}); }}")
    # 1d. element = getter(); if (element) element->method(k);
    r = m(rf"call {H} ; test eax,eax ; je {H} ; push {H} ; mov ecx,eax ; call {H} ; ret")
    if r:
        k = int(r[3], 16)
        return (f"struct {I} {{ void f(int k); }};\n{I}* {Z}_get();\n"
                f"void {Z}() {{ {I}* e = {Z}_get(); if (e) e->f({k:#x}); }}")
    # 1e. element = getter(); if (element) element->slot();
    r = m(rf"call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; jmp dword \[edx\+{H}\] ; ret")
    if r:
        slot = int(r[3], 16) // 4
        return f"{iface(I, slot)}\n{I}* {Z}_get();\nvoid {Z}() {{ {I}* e = {Z}_get(); if (e) e->f(); }}"
    # 2. free(k);
    r = m(rf"push {H} ; call {H} ; pop ecx ; ret")
    if r:
        return f"void {Z}_callee(int k);\nvoid {Z}() {{ {Z}_callee({int(r[1], 16):#x}); }}"
    # 2b. g_flag = v; free(k);
    r = m(rf"push {H} ; mov byte {H},{H} ; call {H} ; pop ecx ; ret")
    if r:
        k, g, v = int(r[1], 16), int(r[2], 16), int(r[3], 16)
        return (f"extern unsigned char g_{g:x};\nvoid {Z}_callee(int k);\n"
                f"void {Z}() {{ g_{g:x} = {v:#x}; {Z}_callee({k:#x}); }}")
    # 2c. g.method(k);
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; ret")
    if r:
        k, g = int(r[1], 16), int(r[2], 16)
        return (f"struct {Z}_G {{ void f(int k); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}() {{ g_{g:x}_{va:x}.f({k:#x}); }}")
    # 3. this->method(b, &a->member)
    r = m(rf"mov eax,dword \[esp\+0x4\] ; mov edx,dword \[esp\+0x8\] ; add eax,{H} ; push eax ; push edx ; call {H} ; ret 0x8")
    if r:
        off = int(r[1], 16)
        return (f"struct {Z} {{ void g(int b, char* a); void f(char* a, int b); }};\n"
                f"void {Z}::f(char* a, int b) {{ g(b, a + {off:#x}); }}")
    # 3b. this->method(a, b)
    r = m(rf"mov eax,dword \[esp\+0x8\] ; mov edx,dword \[esp\+0x4\] ; push eax ; push edx ; call {H} ; ret 0x8")
    if r:
        return (f"struct {Z} {{ void g(int a, int b); void f(int a, int b); }};\n"
                f"void {Z}::f(int a, int b) {{ g(a, b); }}")
    # 3c. member.method(a)   (member object at +off)
    r = m(rf"mov eax,dword \[esp\+0x4\] ; add ecx,{H} ; push eax ; call {H} ; ret 0x4")
    if r:
        off = int(r[1], 16)
        return (f"struct {Z}_M {{ void g(int a); }};\nstruct {Z} {{ char pad[{off:#x}]; {Z}_M m; void f(int a); }};\n"
                f"void {Z}::f(int a) {{ m.g(a); }}")
    # 5. m_ptr->method(a)
    r = m(rf"mov eax,dword \[esp\+0x4\] ; mov ecx,dword \[ecx\+{H}\] ; push eax ; call {H} ; ret 0x4")
    if r:
        off = int(r[1], 16)
        return (f"struct {Z}_M {{ void g(int a); }};\nstruct {Z} {{ char pad[{off:#x}]; {Z}_M* m; void f(int a); }};\n"
                f"void {Z}::f(int a) {{ m->g(a); }}")
    # 6. return m_ptr ? m_ptr->slot() : 0;  (int / bool)
    r = m(rf"mov ecx,dword \[ecx\+{H}\] ; test ecx,ecx ; je {H} ; mov eax,dword \[ecx\] ; jmp dword \[eax\+{H}\] ; xor (eax,eax|al,al) ; ret")
    if r:
        off, slot = int(r[1], 16), int(r[3], 16) // 4
        t = "int" if r[4] == "eax,eax" else "bool"
        return (f"{iface(I, slot, t)}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; {t} f(); }};\n"
                f"{t} {Z}::f() {{ if (m) return m->f(); return 0; }}")
    # 12. if (m_ptr) m_ptr->slot();
    r = m(rf"mov ecx,dword \[ecx\+{H}\] ; test ecx,ecx ; je {H} ; mov eax,dword \[ecx\] ; jmp dword \[eax\+{H}\] ; ret")
    if r:
        off, slot = int(r[1], 16), int(r[3], 16) // 4
        return (f"{iface(I, slot)}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; void f(); }};\n"
                f"void {Z}::f() {{ if (m) m->f(); }}")
    # 11. if (m_ptr) m_ptr->slot(a);
    r = m(rf"mov ecx,dword \[ecx\+{H}\] ; test ecx,ecx ; je {H} ; mov edx,dword \[esp\+0x4\] ; mov eax,dword \[ecx\] ; push edx ; call dword \[eax\+{H}\] ; ret 0x4")
    if r:
        off, slot = int(r[1], 16), int(r[3], 16) // 4
        return (f"{iface(I, slot, 'void', 'int a')}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; void f(int a); }};\n"
                f"void {Z}::f(int a) {{ if (m) m->f(a); }}")
    # 9. this->slot();
    r = m(rf"mov eax,dword \[ecx\] ; jmp dword \[eax\+{H}\]")
    if r:
        slot = int(r[1], 16) // 4
        return (f"struct {Z} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void v(); void f(); }};\n"
                f"void {Z}::f() {{ v(); }}")
    # 16. m_ptr->slot();
    r = m(rf"mov ecx,dword \[ecx\+{H}\] ; mov eax,dword \[ecx\] ; jmp dword \[eax\+{H}\]")
    if r:
        off, slot = int(r[1], 16), int(r[2], 16) // 4
        return (f"{iface(I, slot)}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; void f(); }};\n"
                f"void {Z}::f() {{ m->f(); }}")
    # 13. return m_ptr->m_x;   (dword / byte)
    r = m(rf"mov eax,dword \[ecx\+{H}\] ; mov (eax|al),(dword|byte) \[eax(?:\+{H})?\] ; ret")
    if r:
        off, off2 = int(r[1], 16), int(r[4] or "0", 16)
        t = "int" if r[2] == "eax" else "char"
        pad2 = f"char pad[{off2:#x}]; " if off2 else ""
        return (f"struct {Z}_M {{ {pad2}{t} x; }};\nstruct {Z} {{ char pad[{off:#x}]; {Z}_M* m; {t} f(); }};\n"
                f"{t} {Z}::f() {{ return m->x; }}")
    # 15. this->slot(c, b, a) with constants
    r = m(rf"mov eax,dword \[ecx\] ; push {H} ; push {H} ; push {H} ; call dword \[eax\+{H}\] ; ret")
    if r:
        a3, a2, a1, slot = int(r[1], 16), int(r[2], 16), int(r[3], 16), int(r[4], 16) // 4
        return (f"struct {Z} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void v(int a, int b, int c); void f(); }};\n"
                f"void {Z}::f() {{ v({a1:#x}, {a2:#x}, {a3:#x}); }}")
    # 15b. this->slot(k)
    r = m(rf"mov eax,dword \[ecx\] ; push {H} ; call dword \[eax\+{H}\] ; ret")
    if r:
        k, slot = int(r[1], 16), int(r[2], 16) // 4
        return (f"struct {Z} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void v(int a); void f(); }};\n"
                f"void {Z}::f() {{ v({k:#x}); }}")
    # bool: return m_x != 0
    r = m(rf"mov eax,dword \[ecx\+{H}\] ; test eax,eax ; setne al ; ret")
    if r:
        off = int(r[1], 16)
        return f"struct {Z} {{ char pad[{off:#x}]; int m; bool f(); }};\nbool {Z}::f() {{ return m != 0; }}"
    # stores of constants to three byte globals
    r = m(rf"mov byte {H},{H} ; mov byte {H},{H} ; mov byte {H},{H} ; ret")
    if r:
        g = [(int(r[i], 16), int(r[i + 1], 16)) for i in (1, 3, 5)]
        decl = "".join(f"extern unsigned char g_{a:x};\n" for a, _ in g)
        return decl + f"void {Z}() {{ " + " ".join(f"g_{a:x} = {v:#x};" for a, v in g) + " }"
    # x = cfree(k); return x ? x->method(this) : 0;
    r = m(rf"push esi ; mov esi,ecx ; push {H} ; call {H} ; add esp,0x4 ; test eax,eax ; je {H} ; push esi ; mov ecx,eax ; call {H} ; pop esi ; ret ; xor eax,eax ; pop esi ; ret")
    if r:
        k = int(r[1], 16)
        return (f"struct {Z};\nstruct {I} {{ int g({Z}* owner); }};\n{I}* {Z}_find(int k);\n"
                f"struct {Z} {{ int f(); }};\nint {Z}::f() {{ {I}* x = {Z}_find({k:#x}); if (x) return x->g(this); return 0; }}")
    # int v = 0; m_obj.get(k, g_x, &v); return v;
    r = m(rf"push ecx ; mov edx,dword {H} ; lea eax,\[esp\] ; push eax ; mov eax,{H} ; push edx ; push eax ; add ecx,{H} ; mov dword \[esp\+0xc\],0x0 ; call {H} ; mov eax,dword \[esp\] ; pop ecx ; ret")
    if r:
        g, k, off = int(r[1], 16), int(r[2], 16), int(r[3], 16)
        kk = f"{k:#x}" if k < 0x400000 else f"g_{k:x}"      # mov eax,[g] (normalised text hides ds:)
        decl = f"extern int g_{k:x};\n" if k >= 0x400000 else ""
        kt = "int"
        return (decl + f"extern int g_{g:x};\nstruct {Z}_M {{ void get({kt} k, int g, int* out); }};\n"
                f"struct {Z} {{ char pad[{off:#x}]; {Z}_M m; int f(); }};\n"
                f"int {Z}::f() {{ int v = 0; m.get({kk}, g_{g:x}, &v); return v; }}")
    # BOOL isKindOf(t) { return t == &s_type || Base::isKindOf(t); }
    r = m(rf"mov eax,dword \[esp\+0x4\] ; cmp eax,{H} ; je {H} ; push eax ; call {H} ; test al,al ; je {H} ; mov eax,0x1 ; ret 0x4 ; xor eax,eax ; ret 0x4")
    if r:
        t = int(r[1], 16)
        return (f"extern char g_{t:x};\nstruct {Z}_B {{ bool isKindOf(const void* t); }};\n"
                f"struct {Z} : {Z}_B {{ int f(const void* t); }};\n"
                f"int {Z}::f(const void* t) {{ return t == &g_{t:x} || {Z}_B::isKindOf(t); }}")
    # this->slot(k1, k2, m_a->m_b)
    r = m(rf"mov edx,dword \[ecx\+{H}\] ; mov eax,dword \[ecx\] ; mov edx,dword \[edx\+{H}\] ; push edx ; push {H} ; push {H} ; call dword \[eax\+{H}\] ; ret")
    if r:
        o1, o2, k2, k1, slot = int(r[1], 16), int(r[2], 16), int(r[3], 16), int(r[4], 16), int(r[5], 16) // 4
        return (f"struct {Z}_M {{ char pad[{o2:#x}]; int x; }};\n"
                f"struct {Z} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void v(int a, int b, int c); char pad[{o1 - 4:#x}]; {Z}_M* m; void f(); }};\n"
                f"void {Z}::f() {{ v({k1:#x}, {k2:#x}, m->x); }}")
    # return m ? m->x : 0;
    r = m(rf"mov eax,dword \[ecx\+{H}\] ; test eax,eax ; je {H} ; mov eax,dword \[eax\+{H}\] ; ret ; xor eax,eax ; ret")
    if r:
        off, off2 = int(r[1], 16), int(r[3], 16)
        return (f"struct {Z}_M {{ char pad[{off2:#x}]; int x; }};\nstruct {Z} {{ char pad[{off:#x}]; {Z}_M* m; int f(); }};\n"
                f"int {Z}::f() {{ if (m) return m->x; return 0; }}")
    # BOOL: return m != 0;
    r = m(rf"mov edx,dword \[ecx\+{H}\] ; xor eax,eax ; test edx,edx ; setne al ; ret")
    if r:
        off = int(r[1], 16)
        return f"struct {Z} {{ char pad[{off:#x}]; int m; int f(); }};\nint {Z}::f() {{ return m != 0; }}"
    # this->slot(a, m_x, k)
    r = m(rf"mov edx,dword \[ecx\+{H}\] ; mov eax,dword \[ecx\] ; push {H} ; push edx ; mov edx,dword \[esp\+0xc\] ; push edx ; call dword \[eax\+{H}\] ; ret 0x4")
    if r:
        off, k, slot = int(r[1], 16), int(r[2], 16), int(r[3], 16) // 4
        return (f"struct {Z} {{{''.join(f' virtual void p{i}();' for i in range(slot))} virtual void v(int a, int b, int c); char pad[{off - 4:#x}]; int m; void f(int a); }};\n"
                f"void {Z}::f(int a) {{ v(a, m, {k:#x}); }}")
    # p = arg; this->g(p); return p;
    r = m(rf"push esi ; mov esi,dword \[esp\+0x8\] ; push esi ; call {H} ; mov eax,esi ; pop esi ; ret 0x4")
    if r:
        return f"struct {Z} {{ void g(int* p); int* f(int* p); }};\nint* {Z}::f(int* p) {{ g(p); return p; }}"
    # e = g.find(id); if (e) e->slot(a, k);
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; mov ecx,dword \[esp\+0x4\] ; mov edx,dword \[eax\] ; push {H} ; push ecx ; mov ecx,eax ; call dword \[edx\+{H}\] ; ret")
    if r:
        idv, g, k, slot = int(r[1], 16), int(r[2], 16), int(r[5], 16), int(r[6], 16) // 4
        return (f"{iface(I, slot, 'void', 'int a, int b')}\nstruct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}(int a) {{ {I}* e = g_{g:x}_{va:x}.find({idv:#x}); if (e) e->f(a, {k:#x}); }}")
    # e = g.find(id); if (e) e->slot(); cfree(k);
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; call dword \[edx\+{H}\] ; push {H} ; call {H} ; pop ecx ; ret")
    if r:
        idv, g, slot, k = int(r[1], 16), int(r[2], 16), int(r[5], 16) // 4, int(r[6], 16)
        return (f"{iface(I, slot)}\nstruct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\nvoid {Z}_callee(int k);\n"
                f"void {Z}() {{ {I}* e = g_{g:x}_{va:x}.find({idv:#x}); if (e) e->f(); {Z}_callee({k:#x}); }}")
    # two lookups, each calling a slot
    r = m(rf"push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; call dword \[edx\+{H}\] ; push {H} ; mov ecx,{H} ; call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; jmp dword \[edx\+{H}\] ; ret")
    if r:
        id1, g, s1, id2, s2 = int(r[1], 16), int(r[2], 16), int(r[5], 16) // 4, int(r[6], 16), int(r[10], 16) // 4
        if int(r[7], 16) != g: return None
        return (f"{iface(I + '1', s1)}\n{iface(I + '2', s2)}\nstruct {Z}_G {{ {I}1* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}() {{ {I}1* e = g_{g:x}_{va:x}.find({id1:#x}); if (e) e->f(); "
                f"{I}2* e2 = ({I}2*)g_{g:x}_{va:x}.find({id2:#x}); if (e2) e2->f(); }}")
    # three byte globals = same value
    r = m(rf"(?:mov al,{H}|xor al,al) ; mov {H},al ; mov {H},al ; mov {H},al ; ret")
    if r:
        v = int(r[1], 16) if r[1] else 0
        g = [int(r[i], 16) for i in (2, 3, 4)]
        decl = "".join(f"extern unsigned char g_{a:x};\n" for a in g)
        return decl + f"void {Z}() {{ " + " ".join(f"g_{a:x} = {v:#x};" for a in g) + " }"
    # one byte global = value
    r = m(rf"mov byte {H},{H} ; ret")
    if r:
        g, v = int(r[1], 16), int(r[2], 16)
        return f"extern unsigned char g_{g:x};\nvoid {Z}() {{ g_{g:x} = {v:#x}; }}"
    # this->a(); this->b();
    r = m(rf"push esi ; mov esi,ecx ; call {H} ; mov ecx,esi ; call {H} ; pop esi ; ret")
    if r:
        return f"struct {Z} {{ void a(); void b(); void f(); }};\nvoid {Z}::f() {{ a(); b(); }}"
    # e = g.find(id-arg); if (e) e->slot();
    r = m(rf"mov eax,dword \[esp\+0x4\] ; mov ecx,{H} ; push eax ; call {H} ; test eax,eax ; je {H} ; mov edx,dword \[eax\] ; mov ecx,eax ; jmp dword \[edx\+{H}\] ; ret")
    if r:
        g, slot = int(r[1], 16), int(r[4], 16) // 4
        return (f"{iface(I, slot)}\nstruct {Z}_G {{ {I}* find(int id); }};\nextern {Z}_G g_{g:x}_{va:x};\n"
                f"void {Z}(int id) {{ {I}* e = g_{g:x}_{va:x}.find(id); if (e) e->f(); }}")
    # cfree(a, b, k)
    r = m(rf"push {H} ; push dword \[esp\+0xc\] ; push dword \[esp\+0xc\] ; call {H} ; add esp,0xc ; ret")
    if r:
        k = int(r[1], 16)
        if k >= 0x400000:
            return (f"extern char g_{k:x};\nvoid {Z}_callee(int a, int b, char* k);\n"
                    f"void {Z}(int a, int b) {{ {Z}_callee(a, b, &g_{k:x}); }}")
        return f"void {Z}_callee(int a, int b, int k);\nvoid {Z}(int a, int b) {{ {Z}_callee(a, b, {k:#x}); }}"
    # g_flag = cfree();
    r = m(rf"call {H} ; mov {H},al ; ret")
    if r:
        g = int(r[2], 16)
        return f"extern bool g_{g:x};\nbool {Z}_callee();\nvoid {Z}() {{ g_{g:x} = {Z}_callee(); }}"
    # scalar deleting destructor of a class whose (inline) destructor only resets the vptr
    r = m(rf"mov al,byte \[esp\+0x4\] ; push esi ; mov esi,ecx ; test al,0x1 ; mov dword \[esi\],{H} ; je {H} ; push esi ; call {H} ; add esp,0x4 ; mov eax,esi ; pop esi ; ret 0x4")
    if r:
        return (f"struct {Z} {{ virtual ~{Z}() {{}} virtual void key(); }};\nvoid {Z}::key() {{}}\n"
                f"{Z}* {Z}_make() {{ return new {Z}; }}     // makes VC6 emit the vtable and ??_G")
    # derived ctor that only forwards its arguments to the base ctor
    r = m(rf"(.*) ; mov ecx,esi ; call {H} ; mov dword \[esi\],{H} ; mov eax,esi ; pop esi ; ret (0x[0-9a-f]+)")
    if r:
        n = int(r[4], 16) // 4
        if 1 <= n <= 4:
            a = argl(n)
            return (f"struct {Z}_B {{ {Z}_B({a}); virtual void bkey(); }};\nstruct {Z} : {Z}_B {{ {Z}({a}); virtual void key(); }};\n"
                    f"{Z}::{Z}({a}) : {Z}_B({', '.join(f'a{i}' for i in range(n))}) {{}}")
    # several calls  g.method(k1, k2, ...) on global objects with constant arguments
    calls = re.findall(r"((?:push [^;]+ ; )+)mov ecx,0x([0-9a-f]+) ; call 0x[0-9a-f]+ ; ", s + " ; ")
    if re.fullmatch(r"(?:(?:push 0x[0-9a-f]+ ; )+mov ecx,0x[0-9a-f]+ ; call 0x[0-9a-f]+ ; )+ret", s):
        decls, body, ms = set(), [], []
        for j, (pushes, g) in enumerate(calls):
            vals = [int(x, 16) for x in re.findall(r"push 0x([0-9a-f]+)", pushes)][::-1]
            g = int(g, 16)
            decls.add(f"extern {Z}_G g_{g:x}_{va:x};")
            ms.append(f"void m{j}({argl(len(vals))});")
            body.append(f"g_{g:x}_{va:x}.m{j}({', '.join(cval(v, decls) for v in vals)});")
        if len({g for _, g in calls}) != 1: return None
        return (f"struct {Z}_G {{ {' '.join(ms)} }};\n" + "\n".join(sorted(decls)) +
                f"\nvoid {Z}() {{ {' '.join(body)} }}")
    # UIControl subclass: setFlag(k, on) (BBT-inlined, body in ui.uicontrol.obj) then a member call
    r = m(rf"push esi ; push (0x[01]) ; mov esi,ecx ; push {H} ; sub esp,0x4 ; cmp byte \[esp\+0x8\],0x1 ; .* ; mov ecx,esi ; call {H} ; pop esi ; ret ; .*")
    if r and s.count("call") == 1:
        on, k = int(r[1], 16), int(r[2], 16)
        return (f"struct {Z} : UIControl {{ void g(); void f(); }};\n"
                f"void {Z}::f() {{ setFlag({k:#x}, {'true' if on else 'false'}); g(); }}")
    # sequence of: e = g.find(id); if (e) { e->setFlag(k, on); e->slot(); }
    blk = (r"push 0x([0-9a-f]+) ; mov ecx,0x([0-9a-f]+) ; call 0x[0-9a-f]+ ; mov esi,eax ; test esi,esi ; je 0x[0-9a-f]+ ; "
           r"push 0x([01]) ; push 0x([0-9a-f]+) ; mov ecx,esi ; sub esp,0x4 ; cmp byte \[esp\+0x8\],0x1 ; je 0x[0-9a-f]+ ; "
           r"mov edx,dword \[esp\+0x4\] ; mov eax,dword \[ecx\+0x7c\] ; not edx ; and eax,edx ; mov dword \[ecx\+0x7c\],eax ; "
           r"add esp,0xc ; mov e[a-d]x,dword \[esi\] ; mov ecx,esi ; call dword \[e[a-d]x\+0x([0-9a-f]+)\] ; ")
    r = re.match(rf"push esi ; ((?:{blk})+)pop esi ; ret", s)
    if r:
        bl = re.findall(blk, r[1])
        gs = {b[1] for b in bl}
        if len(gs) != 1: return None
        g = int(bl[0][1], 16)
        out = [f"struct {Z}_G {{ UIControl* find(int id); }};", f"extern {Z}_G g_{g:x}_{va:x};"]
        body = []
        for j, (idv, _, on, k, slot) in enumerate(bl):
            sl = int(slot, 16) // 4
            out.append(f"struct {I}{j} : UIControl {{{''.join(f' virtual void p{i}();' for i in range(1, sl))} virtual void f(); }};")
            body.append(f"{I}{j}* e{j} = ({I}{j}*)g_{g:x}_{va:x}.find({int(idv, 16):#x}); "
                        f"if (e{j}) {{ e{j}->setFlag({int(k, 16):#x}, {'true' if on == '1' else 'false'}); e{j}->f(); }}")
        return "\n".join(out) + f"\nvoid {Z}() {{\n    " + "\n    ".join(body) + "\n}"
    # checked cast of a member, then a virtual call / field read on the result (null not handled)
    r = m(rf"push esi ; mov esi,dword \[ecx\+{H}\] ; test esi,esi ; je {H} ; mov eax,dword \[esi\] ; push {H} ; mov ecx,esi ; call dword \[eax\+{H}\] ; test al,al ; je {H} ; (.*)")
    if r:
        off, k, s1, rest = int(r[1], 16), int(r[3], 16), int(r[4], 16) // 4, r[6]
        cls = (f"struct {I} {{{''.join(f' virtual void p{i}();' for i in range(s1))} virtual bool isKindOf(int t);")
        q = f"{I}* p = m; {I}* q = (p && p->isKindOf({k:#x})) ? p : 0;"
        t = re.fullmatch(rf"mov ecx,esi ; mov edx,dword \[ecx\] ; call dword \[edx\+{H}\] ; pop esi ; ret ; xor ecx,ecx ; mov edx,dword \[ecx\] ; call dword \[edx\+{H}\] ; pop esi ; ret", rest)
        if t and t[1] == t[2]:
            s2 = int(t[1], 16) // 4
            if s2 <= s1: return None
            cls += "".join(f" virtual void p{i}();" for i in range(s1 + 1, s2)) + " virtual void g(); };"
            return f"{cls}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; void f(); }};\nvoid {Z}::f() {{ {q} q->g(); }}"
        t = re.fullmatch(rf"mov (eax|ax),(dword|word) \[esi\+{H}\] ; pop esi ; ret ; xor eax,eax ; pop esi ; mov (?:eax|ax),(?:dword|word) \[eax\+{H}\] ; ret", rest)
        if t and t[3] == t[4]:
            fo = int(t[3], 16); ty = "int" if t[1] == "eax" else "short"
            cls += f" char pad[{fo - 4:#x}]; {ty} x; }};"
            return f"{cls}\nstruct {Z} {{ char pad[{off:#x}]; {I}* m; {ty} f(); }};\n{ty} {Z}::f() {{ {q} return q->x; }}"
        return None
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", help="built .obj: add matches to Notes/zoo.map, record failures")
    ap.add_argument("--with", dest="extra", action="append", default=[], help="objects with callees (e.g. ui.uicontrol.obj)")
    ap.add_argument("--max-size", type=int, default=400)
    a = ap.parse_args()
    if a.check:
        return check(a.check, a.extra)
    import csv
    inv = {int(r["va"], 16): int(r["size"]) for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "inventory.csv")))}
    failed = set()
    if os.path.exists(FAILED):
        failed = {int(x, 16) for x in open(FAILED).read().split()}
    class Arg: pass
    parts = []
    for img, mod, va, name, st in TR.zoo_functions(Arg()):
        if not (st == "todo" or (name.startswith("?") and f"Z_{va:X}" in name)): continue
        if va in failed or inv.get(va, 999) > a.max_size: continue
        ins, ok = TR.walk(img, va)
        if not ins or not ok: continue
        if TR.recognise(img, ins): continue                 # gentrivial.py's job
        c = gen(va, " ; ".join(T.norm(t) for _, _, t in ins))
        if c: parts.append(f"// {va:#x}\n{c}\n")
    hdr = ("// Small forwarding functions of zoo.exe whose owners are not known yet (Tools/genshapes.py).\n"
           "// Z_<va>... are placeholders; move each function to its real class when identified.\n\n#pragma pack(1)\n\n"
           "struct UIControl { virtual void v0(); void setFlag(unsigned long flag, bool on); };   // Src/ui/uicontrol.cpp\n\n")
    open(OUT, "w").write(hdr + "\n".join(parts))
    print(len(parts), "functions written to", OUT)

def check(objpath, extra=()):
    from compare import PE, Disasm, OrigCode, Obj, compare_function, Mismatch, register_obj, enable_symcheck
    pe = PE(os.path.join(ROOT, "Original", "zoo.exe")); dis = Disasm(); orig = OrigCode(pe, dis)
    enable_symcheck(os.path.join(ROOT, "Original", "zoo.exe"))
    obj = Obj(objpath); register_obj(obj)
    for e in extra: register_obj(Obj(e))
    mp = os.path.join(ROOT, "Notes", "zoo.map"); have = open(mp).read()
    good, bad = [], []
    for k, (sec, val, name) in enumerate(obj.funcs):
        mm = re.match(r"^(?:\?(?!key@)[A-Za-z0-9_]+@[ZK]_([0-9A-F]+)@@|\?Z_([0-9A-F]+)@@Y|\?\?(?:_G|0)Z_([0-9A-F]+)@@|\?UIH_([0-9A-F]+)@@Y)", name)
        if not mm: continue
        va = int(mm.group(1) or mm.group(2) or mm.group(3) or mm.group(4), 16)
        try:
            compare_function(obj, k, va, orig, dis); good.append((name, va))
        except Mismatch:
            bad.append(va)
    add = [f"{n} = {va:#x}" for n, va in good if n not in have]
    open(mp, "a").write("".join(x + "\n" for x in add))
    prev = open(FAILED).read().split() if os.path.exists(FAILED) else []
    open(FAILED, "w").write("\n".join(sorted(set(prev) | {f"{v:#x}" for v in bad})) + "\n")
    print(f"{len(good)} match ({len(add)} new map lines), {len(bad)} failed -> {FAILED}")

if __name__ == "__main__":
    main()
