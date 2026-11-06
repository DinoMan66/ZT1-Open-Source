# Zoo Tycoon matching notes

## Target facts
- zoo.exe v12.4.0.9, PE timestamp 2002-09-24, image base 0x400000, entry 0x4CBD36.
- Source root `C:\aqua\src\` ("aqua" = Marine Mania codename). Subsystem folders seen in assert strings:
  gx, snd, UI, movie, http (e.g. `C:\aqua\src\gx\gxcanvas.cpp`, `C:\aqua\src\snd\dx8sndmgr.cpp`).
- No RTTI (/GR-), no C++ EH (no __CxxFrameHandler), static single-threaded CRT (libc).
- Managers are created by name from zoo.ini [mgr]: ZTAIMgr, ZTWorldMgr, BFGameMgr, ZTScenarioMgr,
  BFScriptMgr, BFSoundMgr, ZTAdvTerrainMgr.

## Rich header (count of objects per tool)
| prodid | tool | build | count | meaning |
|---|---|---|---|---|
| 11 | C++ compiler | 8447 | 290 | game C++ (~290 .cpp files) |
| 10 | C compiler | 8447 | 9 | game C files |
| 10 / 11 | C / C++ | 8168 | 153 / 3 | VC6 RTM static CRT (libc.lib) |
| 14 | MASM 6.13 | 7299 | 29 | CRT assembly |
| 28 / 29 | VC7.0-beta C / C++ | 8830 | 1 / 2 | prebuilt third-party lib (not game code) |
| 4 | Linker 6.00 | 8447 | 5 | |
| 6 | cvtres | 1735 | 1 | resources |

## BBT-style layout
- Cold blocks live far away and jump back; conditions can be inverted; jmps inserted or removed.
- No padding between functions (no int3/nop alignment).
- compare.py handles this by walking the CFG. Untested parts: switch jump tables.

## Toolchain (verified 2026-10-18, rounds 002-006)
- Compiler = VC6 + SP3: RTM cl.exe/c2.dll (12.00.8168) + SP3 c1.dll/c1xx.dll. Our objects carry
  @comp.id 000B20FF (C++ build 8447), identical to the game's 290 C++ objects.
- Installed in the VM at C:\VC6SP3\Bin (English files from the SP3 CD); build_core.bat uses it automatically.
- Flags: `/O2` (default /GB). Sweep on BFLog.cpp: /Ox, /G3, /G4, /G5 give identical code;
  /Oy-, /O1, /Ob2, /G6, /Og- break matches. So: /O2, frame-pointer omission on, inline only `inline`.
- VC6 pads functions with nops to 16 bytes in the .obj; BBT removed the padding in zoo.exe (compare.py ignores it).

## Compiler habits learned
1. strlen/strcat/strcpy are intrinsics under /O2 (repne scasb / rep movsd+movsb) - write plain strcat.
2. Sparse switches (3,6,9,12,15) become a byte index table + jump table, exactly like the original.
3. A ternary feeding one call (`f(x ? a : b)`) gives `mov eax,a; test; jne; mov eax,b` - matches.
4. VC6 shrink-wraps callee-saved pushes into an `if` body when the function is one big if; the
   original sometimes does not (BFLogHResult) - cause still unknown.
5. SOLVED (round 030): `sub esp,4; <tiny body>; add esp,4+n` after pushed arguments is NOT the compiler -
   the post-link optimizer (BBT) inlined a call to a tiny function (it reserves the return-address slot,
   runs the body, then pops return address + arguments). Write a normal call; compare.py now expands it
   (bbt_inlined_call: the callee must be defined in our object, straight-line). Seen for
   _STL_alloc_proxy's constructor in every std::string(const char*) and in BFLogV.

## Codebase facts
- Logging: BFLog(file, line, hrLevel, level, delta, hr, hasHr, fmt, ...) is called by a macro with
  __FILE__/__LINE__; delta comes from a global (0x638054, probably zoo.ini deltaLog*), cutoff 0x63804C.
  Levels TRACE=3 INFO=6 NOTE=9 ERROR=12 FATAL=15; level >= 100 suppresses the "file(line)" prefix.
- 0x4010C7 returns a global app/game object (0x638148) whose HWND is at +0x4C4.
- 0x603505 maps DirectX HRESULTs to strings (likely DXGetErrorString8 from dxerr8.lib - the Utc13 objects).
- Hundreds of 187-byte static initialisers build a temporary STL container from a manager name
  ("ZTWorldMgr", "ZTGameMgr", ...) - a header-level static in many .cpp files.
- CRT functions spotted: sprintf 0x40667D, _vsnprintf 0x52B95D, abort 0x629B1C.

## Round 008-012 findings (GXCanvas / GXVidMan)
6. Logging macros: original passes __LINE__; we reproduce it with `#line N` right before the call
   (inside headers too). Plain logs: BFLog(BFLOG_ARGS(level), fmt, ...) with delta g_bfLogDelta;
   HRESULT logs: BFLogHR(BFLOG_HR_ARGS(hr), fmt, ...) = ERROR if FAILED else TRACE.
7. `HRESULT hr = x->Call(); BFLogHR(..hr..)` - never put the call inside the log arguments
   (the original calls first, then pushes the format string).
8. "Success path inside the if": `if (createBltSurfaces()) { log; return true; } return false;`
   gives the shared `xor al,al` failure tail; `if (!f()) return false;` returns al directly.
9. Two consecutive member stores come out in REVERSE order of loads: to get `load +0xC, load +8`
   write `desc.dwWidth = mWidth; desc.dwHeight = mHeight;` (width at +8, height at +0xC).
10. Unused-looking `|=` on a zeroed struct (`desc.ddsCaps.dwCaps |= ...` after memset) is real:
    the original keeps the load/or/store.
11. BOOL -> bool through an inline helper gives neg/sbb/neg (e.g. BFWindow::isMinimized).

## STLport (IMPORTANT for later)
- The game's strings/containers are NOT VC6's Dinkumware STL. String objects are 3 pointers
  (start, finish, end_of_storage) built by a range-init call with a tag argument, and freed through
  deallocate(ptr, size) - that is STLport's layout (_String_base / __node_alloc).
- The `push 0; push &alloc; ...; sub esp,4; mov eax,ecx; mov ecx,[esp+8]; mov [eax],ecx; add esp,0xC`
  sequence before every string construction is the inlined allocator copy for the default argument.
- Needed before matching any string/container code: the exact STLport version (4.0 / 4.5 / 4.5.3)
  and its configuration. Functions: 0x401CAB (range init), 0x401A2F (deallocate), 0x41B55D (ini bool).

## Compiler identification, revised (rounds 020-024)
- Binary versions in the VM: SP3 c1.dll/c1xx.dll = 12.00.8472, SP3 c2.dll = 12.00.8447, cl.exe = 12.00.8168 (RTM).
  SP4: c1/c1xx 12.00.8786 (FileList says 8867), cl.exe 12.00.8804; SP4 ships NO c2.dll (only vb98\c2.exe 8783)
  and its front end refuses the 8447 c2 ("Il mismatch between 'P1' version '19991026' and 'P2' version '19970710'").
- The Rich-header / @comp.id build number (8447) is stamped by **c2.dll**, so: the game's optimizer = 8447 = ours.
- The game's FRONT END (c1xx) is therefore unknown: RTM 8168, SP1/SP2, or SP3 8472. The remaining register-choice and
  `[esp]` vs `[esp+0]` differences suggest it is not SP3's. Next test: RTM c1/c1xx (VS6 Enterprise CD1) + SP3 c2.
- Flag sweep 2 (gxcanvas + dx8sound, 12 flag sets) changed nothing except /G6 (worse). /O2 stays.
- Infrastructure: device_commit_files can re-send an older upload for a stagedPath it has seen before.
  Always stage commits from a unique copy (scratchpad stage.sh -> outputs/_stage/<ns>/...). VirtualBox shared
  folder needed ~5 s before the VM sees new files; build_core.bat now waits before copying Src.

## STLport version = 4.0 (rounds 027-028, 2026-10-21)
- Probe: Src\stltest\stltest.cpp compiled against all seven 4.x releases (headers unpacked in the VM at
  C:\stlport\stl40 ... stl462, from Tools\stlport_headers.zip). Map: Notes\stl_probe.map.
- Configuration the game used: header-only STLport (no prebuilt iostreams library) with the single-threaded
  runtime. Flags per file: `/I C:\stlport\stl40\stlport /D __STL_NO_SGI_IOSTREAMS` (4.5+ spell it
  _STLP_NO_OWN_IOSTREAMS). Without it, 4.0-4.5.1 refuse /ML ("Only multi-threaded runtime library...").
- Result: only 4.0 reproduces __node_alloc<false,0>::allocate (0x40107F, incl. the inlined refill that BBT split
  into 6 cold blocks); 4.0 also matches allocator<char>::deallocate (0x401A2F) and _S_chunk_alloc (0x40355A).
  4.5/4.5.1 mismatch allocate; 4.6.1/4.6.2 mismatch all three; 4.5.3/4.6 do not emit allocate out of line.
- In 4.0 the string's char_traits is the native std:: one (`basic_string<char, std::char_traits<char>, _STL::allocator<char> >`).
- Still to confirm with string code: which game functions are _M_range_initialize (0x401CAB) / _M_allocate_block (0x401D2D);
  4.0 did not emit them out of line in the probe (the probe's uses were inlined).

## Static initialisers (rounds 029-033)
12. BBT also merges a tail jump with its target: VC6 emits `$E17: call $E14; jmp $E16`, the original has
    `call ctor; push dtor; call atexit; pop ecx; ret`. compare.py follows a relocated jmp into the callee
    when it is defined in our object (library targets like _abort are accepted unchecked).
13. Self-registration (886 copies, Notes/instances_registrars.csv): Src/include/BFRegistry.h. Each class
    header has `BF_REGISTER_MGR(cls)` (13 managers, registry 0x5770E5) or `UI_REGISTER(cls)` (17 UI
    classes, registry 0x5774BF); the registrar ctor takes `const std::string&`, so the temporary string
    is built by the caller. Class placeholders: Src/include/registered_classes.h (replace with the real
    headers). Strings and s_registered guards are shared across TUs (defined once).
14. File-static `static const std::string kX("...")` in a header: ctor/dtor/atexit-stub/wrapper shapes
    (Notes/instances_static_init.csv, reference TU Src/reg/static_shapes.cpp). 13 need/building names
    (food, drink, ...) appear in ~42 TUs each. Template statics from the native VC headers
    (ctype<>::id, guard bytes 0x64A6E8/9) and rb-tree header globals produce the other $E functions.
15. Tools/instances.py verifies functions that one source produces many times (va,key[,shape],status).
16. BBT re-encodes every `[reg+0]` as `[reg]`: zoo.exe has 0 disp8=0 memory operands against 154 `[esp]`
    ones, while VC6 emits `[esp+0]`. compare.py accepts the 1-byte-shorter form (same_without_disp0), and
    treats byte-identical epilogue blocks (`pop ecx; ret` twice) as the same block (same_tail).
17. BFLogDebugString (0x52B8C4) exists only as a leftover body: BBT inlined all its calls. More such
    "orphan" helpers will turn up wherever the original shows `sub esp,4` after pushed arguments.
18. BBT inlines whole callees (with branches and loops) across objects, e.g. free() -> __sbh_find_block,
    and pads moved blocks with nops. compare.py walks the callee in place (inline contexts, depth <= 3,
    20,000 steps), skips padding nops, and verifies each BBT duplicate of a block. For a callee in another
    object, load that object too (compare.register_obj; libmatch.py loads whole libraries).
19. CRT: 251 functions found from VC6 RTM LIBC.LIB/LIBCP.LIB (Notes/libmatch.csv). Tiny (<8 bytes) and
    multi-name small hits are dropped as too generic. Unmatched CRT code probably needs the same
    cross-object inlining from objects whose callee is in a DIFFERENT library (kernel32 thunks, etc.).
20. Game translation units include <locale>: every one has the 55-byte initialiser for collate<char>::id and
    ctype<unsigned short>::id (shared guard bytes 0x64A6E8/9) plus two atexit stubs for their empty dtors.
    A TU without <locale> only gets ctype<unsigned short>::id in its own $E (not seen in zoo.exe).
21. Global std::string with EXTERNAL linkage (extern const / class static member / non-const global)
    schedules `lea ecx; mov esi,eax` before the pushes; a file-static `static const` one pushes first.
    Class static members also get a guarded destructor (guard $S, bit 1) - that identifies them.
    The 20 such strings (Overlay, paths, helicopter, filter, maint, tour, guests, ambient, rubble, building,
    food, keeper, animals, staff, fences, objects, tankwall, unit, .ai, entity) look like resource-type
    names of one class each.
22. STL template code: explicit instantiations in Src/stl/*.cpp + `shapescan.py --all` find the game's
    instantiations (same code for any element type of the same size). Functions under 24 bytes are skipped
    (accessors look like every other getter). Hits are matched by code shape; the real element types are
    still unknown (map<int,int>::_M_erase matches 43 different maps).
23. GXLLE blitters (gxlledither.cpp 19, gxlleblend.cpp 14, ~1 KB each): RLE rows (segment count; per segment
    skip byte, count byte, palette indices), a zoom counter that compiles to `if (frac++ == 0) {...} if (frac >= 1)
    frac = 0`, inlined GXCanvas::lockWrite/unlockSurface (mLocked 2 = write-locked). The original keeps one more
    stack local than our drafts (9 dwords: rows, line, height, width, step, count, segments, index byte,
    palette). Its clip loop tests `y + 1 <= 0`. Var builds are free (verdict.py ignores them): explore there,
    rank with Tools/similar.py --regs.
24. create() = `return (Base*)new T;` (push size / operator new / jmp ctor). When the ctor is only reached from
    create(), BBT lays its body right after it and compare.py cannot check it without our ctor: write the ctor
    in the same object (it then compares through), don't touch create().
25. gxlledither progress (rounds 044-048, Var builds): `while (y + 1 <= 0)` gives the original's clip test; writing
    the pixel through a walking pointer (`BYTE* d = dst; *d++ = ...; *d = 0xFF;`) gives the 0x24 frame. Best
    draft: Notes/drafts/gxlledither_best.cpp (61% structural similarity). Left: register assignment.
26. Constructors: members initialised before the vptr store come from the member-init list or from member
    objects (STLport list/vector/map ctors inline completely); body statements come after the vptr store.
    UIControl::setFlag(flag, on) (`if (on == true) m_flags |= flag; else m_flags &= ~flag;`, flags +0x7C) is
    inlined by BBT 185 times; keep it out of line in our object so compare.py can expand it.
27. Runs of zeroed members that the original initialises with a different instruction schedule are member
    STRUCTS with inline ctors (ZTMiniMap: 9-int + 3-int structs). Nesting also changes VC6's inlining: a map
    two structs deep gets its _Rb_tree_base ctor called out of line (as UIGraph's original does) but then
    _M_empty_initialize is not inlined either, unlike the original. Tried (rounds 055, 062-064): nesting 0-2,
    inheritance from map, multimap, map<string,..>, earlier out-of-line use in the TU. Still open.
28. UIElement (root, vtable 0x632258): words +4 = 1, +6 = 0, +8 = ++g_id (0x638D48), all in the init list.
    UIControl (0x50F8E7) : UIElement, size 0xB8; UIImage (0x50FE83) : UIControl, size 0x35C;
    UIView : UIImage adds nothing.
29. UIEditableText ctor (0x510CEE): original frame is 8 bytes - the string's allocator temporary (1 byte) and
    the UIColor(0,0,0xFF) temporary (3 bytes, copied as word + byte into +0xAC) get separate dwords; ours packs
    them into one (frame 4). Temporary, named local, member-wise assignment all give 4 (round 067).
30. BBT also inlines callees that take no stack arguments WITHOUT the `sub esp,4` frame (global vector
    initialisers: `call ctor; jmp atexit-stub` became the ctor body followed by the stub's body). compare.py
    tries such a frameless inline when our `call` meets a non-call in the original.
31. `x = cond ? p : 0;` keeps the zero in a register (`xor eax,eax; mov [m],eax`) while `if (cond) x = p;
    else x = 0;` stores an immediate (`mov [m],0`) (rounds 079-087).
    A local copy of a member (`T* o = m_owner;`) is what keeps it in a callee-saved register across a
    virtual call; an inline helper taking the member as argument re-reads it.
32. Trivial bodies (getters/setters/constants/global addresses, 241) are generated by Tools/gentrivial.py as
    placeholder classes Z_<va> in Src/misc/trivial_unowned.cpp; when you identify the owner, move the function
    into its class and replace the map line (e.g. 0x41226C became ZTAction::~ZTAction).
33. "Action" family (Src/include/ztaction.h): root ctor 0x4139FD / dtor 0x41226C, middle ctor 0x413A43,
    leaf ctors (66) and dtors (74) differ only in vtable and type object -> Notes/instances_actions.csv.
    Every vtable slot 1 returns a class id (0x01..0x86); slot 7 of the entity type object is isKindOf.
34. device_commit_files can deliver a STALE copy when the same file was committed a few minutes earlier
    (round 084 kept the previous ztaction.cpp). If a build result looks unchanged, compare the file size with
    device_list_dir (or stage the source back) before spending an attempt. The outputs folder syncs a few
    seconds behind local writes: wait ~5 s after editing (or commit again) and always check the size.
35. VC6 inlines template member functions even when they are defined outside the class; code that the
    original repeats per type WITHOUT inlining (BFRefData release/set/reset) is therefore per-class
    non-template code (macro BF_REFDATA in Src/include/bfrefdata.h). VC6 does emit tail `jmp` for a call at
    the end of a void function (dtor chains, virtual calls). To list remaining repeated shapes: group the
    todo functions of Notes/inventory.csv by their normalised instruction text (trivial.walk + triage_lib.norm).
36. UI handlers (Src/ui/uihandlers.cpp). Habits that decided matches:
    - `mov ecx,<obj>; mov eax,[ecx+..]` with a cold `xor eax,eax; jmp back` = an out-of-line accessor that BBT
      inlined without a frame (UIListCtl2::selectedId 0x443C1E). Find its orphan body, map it, call it.
    - The original often computes a call's argument into a local before pushing constants:
      `UIControl* item = find(id); x = l->m4179de(item, 1);` (not `m4179de(find(id), 1)`).
    - A two-step null test (`mov eax,esi; xor esi,esi; test eax,eax; je; mov esi,[eax+..]`) is an inline
      helper returning a pointer (iconTypeOf) followed by `int v = 0; if (t) v = t->m;`.
    - `fld [m]; push ecx; fstp [esp]` for a float argument = an inline accessor returning float; a plain
      member passes as `mov eax,[m]; push eax`.
    - `for (i = 0; i < v.size(); ++i)` (size in the condition) gives the original's search loops; hoisting
      size() into a local changes the register allocation.
37. ztaction-style variant builds now use one scratch file per folder (Src/ui/uihandlersVarA.cpp), overwritten
    freely; map variant functions to the target address in a throw-away map and run compare.py directly.
38. `bool f() { if (x <= 0) return true; return false; }` gives `mov eax,[m]; test eax,eax; setbe al`; the
    same as `return x <= 0;` gives `xor eax,eax; cmp; sbb; inc` (unsigned) - the original's out-of-line
    predicates use the if/return form (ZTPager::atFirst/atLast, round 143 variants P1-P6).
39. A call whose `this` is PUSHED after the hidden return pointer (`push args; push retptr; push obj; call;
    add esp,4n`) is a variadic member function (`string ZTGlobal148::format(int id, ...)`, 0x41CA7F):
    variadic members are __cdecl with `this` as the first stack argument.
40. VC6 sinks the push of a callee-saved register below an early exit when the early exit is a separate
    `return` (`if (!e) return found;` in ZTGame::m443ffa 0x443FFA; ebx inside the first if-block of
    UIH_52F686). A common epilogue for the early exit keeps the push in the prologue.
41. Open: UIH_47F0A2 builds `std::string(g_638084)` with the ctor and the allocator ctor inlined but
    _M_allocate_block (0x401D2D) called; every other string-from-char* in our build calls the ctor out of
    line (0x40505A) or inlines everything. Inline wrappers, explicit temporaries and allocator arguments did
    not change it (round 138, VarA1-5). Rounds 169-172 also tried /Ob1, /Ob2, /GX, __STL_NO_EXCEPTIONS,
    __STL_USE_DECLSPEC (+__STL_DESIGNATED_DLL) and `extern template class` / explicit instantiation of
    allocator<char>, _STL_alloc_proxy<char*,..>, _String_base<char,..>: the in-class members stay inlined.
    The same root cause makes `std::string s;` (default ctor) differ: the original calls the alloc-proxy ctor
    0x4012A6 and allocator ctor 0x4010E4 out of line (BBT later inlines some copies) and keeps a separate
    allocator temporary (frame 0x10 vs our 0xC) - UIH_61615A + 5 copies, UIH_618B27.
42. `mov esi,[g_obj]; call key(); push eax; mov ecx,esi; call obj->f` = the object pointer was read into a local
    BEFORE the argument call: `Mgr* m = g_mgr; r = m->f(key());` (UIH_615576, UIH_6156DA). Writing
    `g_mgr->f(key())` loads the global after the call.
43. `mov ecx,<obj>; mov eax,[ecx+off]; ...` at the start of a test, with nothing that needed ecx, is an out-of-line
    accessor BBT inlined without a frame (UIScreen3F8::flag14, UIList398::selectedIndex, ZTGlobal148::setSound).
    Make it an out-of-line member; this also fixed the old failure UIH_4DE496.
44. Local copy first for 3-byte struct assignment: `UIColor col = g_x; c->m_color = col;` loads both parts
    before storing (`mov cx,[g]; mov dl,[g+2]; lea edi,[obj+off]; ...`); `c->m_color = g_x;` interleaves.
45. BBT folds an inlined callee's own `add esp,a` (after a cdecl call inside it, e.g. free() in
    allocator::deallocate) with the `ret n` and the caller's cleanup into one `add esp,a+4+n+caller`.
    compare.py models it (inlined context, our `add esp` directly followed by `ret`).
46. Namespace-scope STLport containers (no guard byte, unlike class statics - MATCHING_NOTES 21) give their
    own $E initialisers/destructors: Src/reg/static_globals2.cpp (map<int,int> dtor x17, list<int> ctor x6,
    + set/list shapes), Notes/instances_globals2.csv. Find more with Tools/shapescan.py on a new reference
    TU (static_globals3.cpp) rather than editing an existing one ($E numbering is the instance key).
47. Out-of-line STLport members are best found by INSTANTIATING them in a throw-away reference TU and
    running Tools/shapescan.py with every function of its object (`--func <name>=<label>` for all, shell
    loop in PROGRESS.md history) and `--max-size 1200`: Src/reg/stl_inst6.cpp (string-keyed trees etc.,
    59 hits), stl_inst7.cpp (POD element sizes 8..64). Element TYPE does not matter, only size and
    copy semantics; never edit a listed TU (keys are its symbol names).
48. A class whose destructor is inline gets no ??_G in our object unless something emits its vtable: give it an
    out-of-line constructor (Src/misc/derivdtor.cpp). Ignore the ??0 "failure" genshapes then reports.
49. UIManager::setFocus 0x44252D (focus pointer +0x10, skips +0x08/+0x0C) and ZTOptions::setMode 0x4AB138 are
    out-of-line members BBT inlines with a `push arg / sub esp,4` frame; write them out of line in the same object.
    UIManagerX::m4fff2c (message box) returns the button id (6 = yes, 2 = cancel).
50. Scratch scorer for any symbol (not only Z_/UIH_ names): compare_function on a chosen symbol substring = VA, as
    in genshapes.check; genshapes --check also accepts any `?member@Z_<va>` / `@K_<va>` name now (not key()).
51. `const std::string& g_ref = std::string(g_chars);` at namespace scope: one $E builds the static temporary
    ($S) inline and stores the reference - cluster 0x57a9e3 x5 (Src/reg/static_globals7.cpp, instances_globals7.csv).
    Here our compiler emits the same `lea ecx,[eax+esi]` order as the original (unlike strreturn.cpp).
52. compare.py does not check the target of a tail `jmp` to a symbol it has no body for: a 5-byte `jmp ext`
    or `mov ecx,imm / jmp ext` "matches" unrelated code (shapescan reported 17 member wrappers as `$E2` and
    3 non-ctor functions for static_globals8). Verify such hits by hand (target VA) before keeping them.
53. Globals whose $E ctor/dtor call the same out-of-line member before/after the container code are objects of
    a small class with inline ctor/dtor calling e.g. reset(): Src/reg/static_globals9.cpp (map<int,set<int>>,
    reset 0x40A5BC, 6 $E). Out-of-line-ctor-only globals: static_globals8.cpp (`mov ecx,g / jmp ctor`).
54. `mov ecx,esi / sub esp,4 / push 0 / push 0x80 / sub esp,4 / <setFlag body>` = BBT inlined a no-argument
    out-of-line wrapper that itself calls setFlag (two levels). Write the wrapper out of line too
    (UIFlag80::clearFlag80 in uihandlers.cpp); compare.py expands nested calls (0x4ef9f1 x4).
55. compare.py treats data relocations to different globals (and offsets) as equal, so one reference $E covers
    every global with the same code; it does NOT distinguish which byte of a UIColor gets the odd value. Pick
    the $E whose store order matches by hand (static_globals11.cpp: UIColor consts, UIColor[6]; globals12: map[3]).
56. Argument copies tell the source shape: `mov ecx,ebx / push 0 / mov edx,edi / push ecx / push edx` (registers
    copied before pushing) = a small non-POD struct passed BY VALUE (UIH_41D565 passes ZTDatePair to the
    (int,int,int,int) function UIH_41D4DF through a second prototype); plain `push ebx / push edi` = separate ints.
    A `push <&buf>` after testing a call's result means the source re-used the buffer, not the returned pointer
    (`if (loadString(id, buf)) c->setText(buf, 0);`, UIH_6158A0) - and re-using the parameter variable for the
    next value (`idx = r->m_textId`) saves the extra callee-saved register.
57. BBT also inlined CRT helpers such as `__ftol` (0x401049: `sub esp,4 / push ebp / mov ebp,esp / fstcw ...`).
    compare.py needs the callee body: pass the library object, `--with Tools/lib/ftol.obj` (extracted from
    LIBC_cd.LIB member ..\build\intel\st_obj\ftol.obj). Three identical calls in an if/else chain that differ
    only in a struct argument are tail-merged by the compiler (one call, three arg-building branches):
    write three calls, not a ternary (UIH_4D9CAE).
58. __FILE__ strings: give the FIRST `#line` marker of each .cpp the original path, `#line 26 "C:\\aqua\\src\\gx\\gxvidman.cpp"`
    (later markers keep it); headers use the path the original compiler saw, `#line 125 "..\\inc\\gxcanvas.h"`.
    Fixed 23 functions whose code already matched (round 238). Get exact paths from the strings in zoo.exe.
59. "Register X held the pointer" with a `mov ecx,[obj]` setup right before an inlined-looking body = a tiny
    out-of-line call that BBT inlined (ecx was the `this` of the call). Look for the surviving out-of-line copy
    (byte search) and write it as a real function: BFWindow::isMinimized 0x4D5FB5 matched GXVidMan::flip,
    which had been "compiler-limited" since round 35.
60. A null test whose register is reused as the return value means an early `return 0;` before the local is
    initialised (DX8Sound::getVolume: `long volume; if (!mBuffer) return 0; volume = 0; ...`).
61. Instance lists only hold copies of OUR shape: a generic two-instruction shape (`mov [ecx],vtable; jmp dtor`)
    also fits unrelated classes. Check the vtable/callee before adding a row - 16 wrong rows were removed
    from instances_actions.csv and 3 re-keyed (LeafB -> LeafA) on 2026-10-28.
