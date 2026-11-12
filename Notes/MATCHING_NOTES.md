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
62. Count loops in the RLE drawers: `test n,n; je` before the loop and `dec n; jne` at its end is
    `for (int n = *src++; n != 0; n--)`; `while (n--)` gives `mov r,n; dec n; test r,r` instead. A loop whose
    entry is `lea eax,[y+1]; test eax,eax; jle` and whose back edge is `inc y; cmp y,-1; jle` is
    `while (y + 1 <= 0)` (`y < 0` gives `test; jge` / `inc; js`, `y <= -1` gives `cmp y,-1` at the entry too).
    Palette reads `mov bl,[eax]; inc eax; mov bl,[eax]; mov al,[eax+1]` are `*p++, *p++, *p`
    (GXLLE::drawDitherMirror32, round 241-242 variants).
63. A "regalloc" difference where the original RELOADS a member the source has just tested (DX8Sound::play
    reloads mBuffer after the attenuation sum) means a call sat in between: the original called a tiny out-of-line
    getter that BBT pasted in without a frame (`mov ecx,[g]; mov eax,[ecx+0x14]`). Look for the same expression in
    a sibling BBT left alone (play(long) at 0x61FD4C still calls 0x404FC0 = DX8SndMgr::getVolume). Writing the
    call matched setVolume, play, playLooped and mute (round 244-246) - they had been filed as "final".
64. `x = -f() - a - b - g()` is folded to `-(f()+a+b+g())`; the original's `neg` then one `sub` per term is a local:
    `long volume = -f(); x = volume - a - b - g();` (DX8Sound::mute).
65. BFLogHResult's callee-saved pushes before the test (instead of shrink-wrapped inside it) came from one
    `strcat` per branch; a shared `text` pointer with one strcat after the if/else gave the shrink-wrapped form.
66. **VC6 inline budget (rounds 249-254).** Whether VC6 inlines STLport's small helpers in a function depends on how
    much OTHER inline work that function has; it is a per-function budget, not a depth limit
    (`#pragma inline_depth(1..4)` probes and /Ob2 never reproduced the original's mix). The budget is spent on the
    function's LATER inline calls first: inline work at the end of a constructor body decides whether the members
    built earlier (std::string, std::map) get _STL_alloc_proxy / _String_base / _Rb_tree_base inlined.
    Symptoms in the original: those helpers called out of line (0x4012A6 alloc proxy, 0x404CF4 _String_base(a,n),
    0x4AB23B _Rb_tree_base(a)) and a separate stack slot for the allocator temporary. Too little inline work in
    our source -> we inline them. UIEditableText's constructor matched once its body had the original's amount:
    the seven stores both its constructors share are an inline helper (resetEditState, 0x510CEE and 0x6201AA),
    plus one more inline call. UIGraph::create matched with its real layout (eight UIColor members at +0x3DC,
    written by init() as 3-byte colours, not 24 bools) plus the same extra inline call: both classes need +0x34E
    set through an inline call (UIImage::setUnk34E). A probe (round 254) showed the extra call could also sit on
    setFlag or the colour store, but not in a user-written UIColor::operator=; the two-class agreement picked
    setUnk34E. UIListBox and ZTMiniMap (also STL members) only match with the plain store.
    The original's out-of-line helpers can also be BBT-inlined back without a frame (`mov ecx,edi` before the
    pasted body: UIGraph's _M_empty_initialize; `mov eax,ecx` + immediates: BFMgr's ctor 0x527EF1 in
    ZTGameMgr::create). Calibrate with throw-away variants (extra inline calls) before guessing the source.
67. A vtable stored by only one constructor, right before that class's own, is a real intermediate base
    (ZTGameMgrBase, 0x6350D0), not BFMgr: BFMgr is 0x6355C0 (1 slot), stored by every manager. Find a hidden base
    constructor by searching the binary for the pasted body (`mov eax,ecx; mov byte [eax+4],0; mov [eax],vt; ret`
    at 0x527EF1 had no callers left: BBT pasted its only call into ZTGameMgr::create).
68. A skipped iteration whose register state the original keeps (GXLLE::drawDitherMirror32: the out-of-range-row
    path does `add ebp,eax` with line in ebp and the pitch still in eax, then jumps straight to the loop test) is
    a branch with its own tail and `continue` (`line += pitch; y++; continue;`), not an if/else joining a shared
    tail. It also moved the function's other variables into the original's registers and stack slots.
69. **The C++ front end is not a factor (rounds 271-274, 2026-11-04).** The VM's C:\VC6RTMFE\Bin holds the RTM
    front end (c1.dll / c1xx.dll 12.00.8168, c1xx 1,183,795 bytes) with SP3's c2.dll 8447; both front ends emit IL
    version 19970710, so they pair with it. A full build (`round-N <time> all VC6RTMFE`) gave code byte-identical to
    the SP3 front end (8472) in all 28 objects, including the STLport-heavy UI files and drawDitherMirror32. Neither
    defines _MSC_FULL_VER (probe). The toolchain is fully accounted for: a remaining difference is source or headers.
70. **Measuring VC6's register weights (rounds 277-282, drawDitherMirror32).** c2.dll's allocator lives in
    regasg.c / color.c (names from its internal-error strings); it is a release build with no dump switches, so
    the weights were measured instead, with throw-away probes (`gProbe[i] = (int)var;` stores, never committed):
    - The swap is a near-tie: ONE extra reference to src inside any loop (top-skip loop, skipped-row branch, row
      loop, segment loop, pixel loop) or THREE outside all loops flips src into edi and dst into ebp, the
      original's assignment. Extra uses of y, x, canvas, rows, dst or line do not.
    - With src flipped, the whole function equals the original except for temporaries in the prologue (which of
      ecx/edx/ebp holds width, rows, the offsets) and the operand order of the skip loops' `lea` (`[edx+edi+1]`
      vs ours `[edi+edx+1]`). The lea order is a side effect of temp allocation: the original non-mirror twin has
      both orders in one function.
    - Weights are counted on the OPTIMISED intermediate code: every source spelling that VC6 normalises to the
      same IL (14 skip-step forms incl. `&src[...]`, int-first sums, split increments, `src[1]`; unsigned/DWORD
      types; an `int zoom = 1;` local; equivalent GXCanvas inlines) gives identical weights and code. A
      value-returning inline row-skip helper LOWERS src's weight; a reference-parameter helper changes nothing.
    So the original's source carries one more loop-level src reference (or one less for its rival) that survives
    VC6's normalisation but emits no extra instruction. Still unidentified.
    Rounds 283-286: from the flipped state, ONE extra in-loop use of almost any other variable (dst, px, frac,
    rows, x, step, canvasWidth, entries, color, height, bpp, locked) flips it back; y, line and canvas do not.
    So it is a many-way near-tie, not src against dst. Changes that alter the IL but not the instructions gave
    nothing: moving px/frac/dst, the loop counters, line, p/d, index or everything to function scope (code
    identical, so the allocator ignores scope and declaration order), and 17 combinations of row-loop
    (`while` / `for (; y < height; y++)` / `for (...; y++, line += pitch)`), top-skip-loop and counter-loop
    (`!= 0` / `> 0` / `while (n--)`) shapes. The prologue's temporaries (the original spills entries before
    loading width and keeps y in its parameter slot) are a SEPARATE difference: the flipped probe keeps them
    at +0x12 with the source's statement order, and 24 prologue orders on top of it did not reproduce them.
71. **How c2.dll (8447) ranks register candidates** (static reading with Ghidra 12.1.4, 2026-11-04; c2.dll is
    itself BBT-optimised, so functions are fragmented). Global allocator driver FUN_1072d3ef, per register class:
    FUN_1072e339 (block pressure), FUN_10722463 (weights), FUN_10723207, FUN_1072450d (priority list), then
    candidates are taken from the list head (DAT_1079d864, linked by +0x14) and given registers.
    - Variable records: hash table DAT_1079d88c[id & 0x3ff], chained by +0x2c; +0x1c id, +0x24 reference count,
      +0x18 raw benefit, +0x3c weight, +0x0c PRIORITY, +0x40 tie-break.
    - Speed mode (/O2, DAT_107ac0b0 set): a reference is worth 1 or 2 (FUN_10722dbc: 2 unless the operand is
      kind 0x0d), times 2^loop_depth (block field +0x6e). weight += benefit * 2^depth.
    - Priority (end of FUN_10722463), per block: P = (live-but-unreferenced count + referenced count + flagged
      live-through count) * 2^depth; each variable referenced in the block gains P * its benefit in that block,
      each variable live in the block without a reference LOSES P. So every block's pressure enters every live
      variable's priority: one extra use of anything moves all of them (the knife edge of note 70).
    - List order: descending +0x0c, ties by descending +0x40 (FUN_1072371a). Physical register order table
      DAT_107adff4 = eax ecx edx esi edi ebx ebp (1 2 3 7 8 4 6; ebp only with frame-pointer omission).
    Probe\weights\ holds a cdb script that dumps the list (run by hand in the VM; not part of the build).
    First dump (2026-11-04, drawDitherMirror32): src is candidate id 21 (29 references, weight 154). Our source:
    id 21 priority 80, behind id 28 (96) and id 12 (83), so it gets ebp. The flip probe raises id 21 to 96, ties
    id 28 and wins the tie (+0x40 0xfb > 0xe2), giving it edi as in the original. Target: +16 priority for src
    relative to id 28. Names (symbol +0x18 -> name string): id 28 = dst, id 12 = bpp, id 27 = frac, id 11 =
    frame, id 32 = p. Our list order: p, temp, frac, frame, dst (96), bpp (83), src (80); flipped: ..., frame,
    src (96, wins the tie with dst), dst, bpp (81). Needed: src above dst and bpp (about +16 against dst).
    Priorities of the rest: canvas -221, y -236, x -320, line -186, step -120, color -22, locked -379.
    Automatic dumps (Tools\queue\cmd_<id>.bat -> Probe\weights\autodump.bat, needs C:\anticheat_allow_cmd.txt in the
    VM; inputs Probe\weights\in\*.cpp, output Results\<name>.weights.txt; summary tool zpri.py) of 61 earlier
    variants: skip-step spellings, types, scope, helpers leave src/dst/bpp at 80/96/83 exactly. Only control
    structure moves them: row loop as `for (; y < height; y++)` src 84; `for (; y < height; y++, line += pitch)`
    src 91 (bpp 113); `src += 2; src += src[-1];` src 96 (different skip code). Next: search loop/block
    structures with the dump as the fitness measure (target: src above dst and bpp, code unchanged).
    Round 291 (17 structural variants, dump + build): row loop while/for/two-update for x rows check
    break/post-decrement/`<= 0`/folded into the condition, skipped row as if/else, top-skip loop as a for.
    Best src 93 (dst 96, bpp 109); every variant that raised src also changed the code, and all of them moved
    the first difference earlier (+0x8) or left it at +0x12. None put src above dst. Round 292 tries where the
    src reads sit (index read before/after the frac branch, `src[1]` skip reads).
    Rounds 292-295: moving `src++` of the pixel read to after the frac branch overshoots (src 208-232, above
    frame/frac, wrong frame). Moving `y++` ahead of the segments in the top-skip loop gives +8 (wrong code: the
    original increments after). FOUND: the skipped-row branch in the original advances `line` and `y` BEFORE
    the segment loop (0x5F160C). Source in that order: src 110 > dst 96 > bpp 83, src edi, y ebp, dst ebp in the
    pixel loop - the original's assignment. Promoted to the main file (round 296). On top of it, 9 variants
    (`src += 1 + count`, `src = src + count + 1`, `*++src`, no count local, line expression orders, rows
    checks) changed nothing or made it worse. What is left is the prologue's scratch registers, the row loop's
    eax/ecx temps and the skip-loop lea operand order.
    Rounds 297-298 (on the round-296 main file): the remaining eax/ecx swap is consistent - wherever the
    original holds y (or the rows counter) in a scratch register it uses ecx and pitch eax; ours is the other
    way round. `y++; line += pitch;` in the row tail gives y ecx there but moves line to eax (multiset 82 -> 80,
    not promoted); the same swap in the skipped row or with `y * lPitch` changes nothing. 40 random orders of
    the prologue statements (dependencies kept) on the new file: none moves the first difference past +0x12
    (best multiset 68 but first difference +0x8). In the original prologue y is stored back to its slot right
    after `y -= yOffset` and ebp is reused for xOffset, then y is reloaded - ours keeps y in ebp and uses ecx.
72. **c2.dll (8447) after the priority list: how registers are actually picked** (Ghidra + cdb, rounds 299-303;
    dump lines from Probe\weights\autodump.bat: G = global pick, T = local pick, B = per-block pick).
    - Driver FUN_1072d3ef walks the priority list; for each candidate FUN_107237a7 computes the registers free over
      its live range and FUN_107245c3 picks one: cost[reg] = sum of copy-preference counts (+0x34 lists) of
      neighbours already holding reg, +100*weight for a neighbour that can only take reg, minus the candidate's own
      preferences; lowest cost wins, ties go to the first register in the order eax ecx edx esi edi ebx ebp.
      EVERY candidate gets a pick, also those with negative priority (they get live-range pieces): in the base
      file x and step get ecx, entries edx, canvasWidth ebp, this ecx, frame eax, src edi, dst ebp, bpp esi.
    - Local values (FUN_10733273): a value copied from a register variable prefers that register (+0x2c, set in
      FUN_107325be); otherwise, in /O2, eax -> ecx -> edx in ROTATION from a pointer (DAT_1079d710) that is reset only
      once per function (FUN_107319ef), skipping registers held by another value or by a global variable live at
      that point (DAT_1079d6c8[reg]); none free -> any register in the order above, then spilling.
    - A second picker FUN_10731ae7/FUN_10732fbc runs per block (rotation index DAT_107ac2dc reset per block, prefers
      registers already used in the function, flag 0x10) for instructions that need a register operand.
    - The logged picks are not all final (e.g. B gives rows edi, the code has ecx), so at least one later pass
      renames/reassigns. Prologue evidence: in the original every value from canvasWidth to x gets edx and xOffset
      gets ebp, i.e. ecx is unavailable for the whole prologue; in ours canvasWidth, rows and xOffset get ecx. Tried
      (rounds 299-301, all no better): `mFrame->` for src / width / xOffset, no `frame` local (4 forms), canvasWidth
      before frame.
    Rounds 305-311 - the prologue is SOLVED (first difference +0x12 -> +0x187). The occupancy log (A lines) shows
    that no scratch register is ever skipped because another local value holds it - every skip is a global
    variable live at that point (DAT_1079d6c8). In the original prologue ecx is skipped from canvasWidth to the x
    adjustment: `step` (a global candidate that gets ecx) is already live, so `int step = -bpp;` comes right after
    bpp, and src is defined before the x/y adjustments (that forces the y spill/reload with ebp the original has).
    Matching order (round 309 search over 42 orders): entries, frame, bpp, step, src, height, canvasWidth, rows,
    `y -= yOffset`, `x += xOffset`. In the main file since round 311. `x = x + ...` vs `+=` and 7 forms of the
    `line` expression make no difference. Next wall: the row-loop header (+0x187) - pitch/y/rows temps eax<->ecx.
    Round 312-314 (on the round-311 file, first difference +0x187 = row-loop header): 15 row-loop variants
    (px/frac/dst declaration orders, rows checks, for-loops, `y++; line += ...`, line declared after the top-skip
    loop) leave +0x187; the rows-check forms make it worse (+0x156). Dumps now name every global pick
    (autoglob.cdb) and list the scratch registers blocked by global variables at each local pick (autoconf.cdb).
    After the main list, c2 re-runs the picker on live-range PIECES: color ebx, step eax (pixel loop), line ebp,
    canvas ebx, height ecx, x edx, y eax (two pieces: the row loop), y ebp (top-skip loop), rows ecx (top-skip
    loop). The original keeps y in ecx in the row loop, so its y piece there picks ecx: eax must be costlier or
    taken by a piece live in the row loop (candidate: step's eax piece). The row-header temps (pitch, y, height)
    are not picked by the local allocator FUN_10733273 at all (no T line for those lines): they follow the pieces.
    Rounds 316-318: the pick cost (FUN_107245c3, DAT_1079d868[reg]) = sum of copy-preference counts (+0x34
    lists of (register, count), e.g. `this` prefers ecx, call results prefer eax) of not-yet-assigned interfering
    candidates that can still take reg, +100*weight for a neighbour with a single choice, minus the candidate's
    own preferences; lowest cost wins, ties go to eax first. For the row loop every relevant piece has cost 0 for
    eax/ecx/edx, so the choice is decided by which registers are still allowed (taken by an interfering piece
    assigned earlier). In the original the row loop keeps pitch (a reused `canvas->mDesc.lPitch` value) in eax
    from the row tail through the loop test into the skipped-row branch, and y/rows/segments in ecx; ours has
    pitch in ecx, so eax is already taken over that range in ours (step's eax piece is NOT the cause: removing step
    from the pixel loops still gives pitch ecx). 12 more row-loop variants (bool loop tests, while forms, reversed
    comparisons, `src[1]` skip reads) keep +0x187.
    Round 320: one shared `segments` / `count` variable (function or row-loop scope, 8 combinations) gives code
    identical to separate loop counters - scope does not reach the allocator. Current reading of the +0x187 wall:
    in the skipped-row block the pitch value (dies at `line += pitch`) and that loop's segments counter (born right
    after) share a block, so they interfere; whichever c2 assigns first takes eax. Ours assigns the segments counter
    in the main list (eax) before the pitch piece (second round -> ecx); the original must assign pitch first.
    Round 321 - the "re-run" decompiled and logged (autoedge.cdb: E lines = the interference neighbours of each
    pick, plus the allowed-register set of every pick). It is not a separate allocator: when a pick leaves some
    candidate with no allowed register, the driver (FUN_1072d3ef) inserts spill code for it (FUN_1073e8f6),
    recomputes weights and priorities for everything still unassigned (FUN_10722463, FUN_10723207), rebuilds the
    list (FUN_1073f9af, ids renumbered) and carries on; allowed sets in that round come from the registers already
    fixed over each live range (FUN_107237a7). In the base file the second round assigns color ebx, step eax,
    line ebp, canvas ebx, two temps, height ecx, x edx, y eax (allowed eax/edx only: ecx is held by an earlier
    piece), y ebp (top-skip), rows ecx (top-skip), y eax. The pitch value of the row loop is NOT a global
    candidate in either round (no temp has its live range: allowed sets show the round-2 temps live in the
    prologue), so its ecx comes from the local/per-block pickers, and the y/rows/segments eax picks follow from
    what pitch leaves free. No source change tried so far (60+ row-loop variants) changes that order.
    Rounds 322-323 - the register passes in order (driver FUN_1076819b): FUN_1072d3ef global allocation (both
    rounds) -> FUN_107319ef local pass (walks every tuple in block-list order: FUN_1073232d frees a register at a
    value's last use, FUN_107323c8 gives a defined value a register - FUN_10733239 keeps one the global pass already
    gave it, otherwise FUN_10733273 = the rotation) -> FUN_10731ae7 per-block pass (/O2 only; only instructions whose
    opcode flag 0x400 asks for a register operand, via FUN_1073311e; its own rotation restarts per block) ->
    FUN_10731e76 frame layout -> FUN_107335b0 -> FUN_1077b958. The row-loop header and loop test get NO local or
    per-block pick at all (no T/B lines for those statements): their registers are the global pass's pieces, so
    the per-block picker is not the cause. Weight<1 candidates go to FUN_10724bb0 instead of FUN_107245c3 (spilled
    or rematerialised, e.g. the pitch load `[canvas+0x14]` re-read at each use). In the original the loop test is
    height ecx / y edx, ours height eax / y edx; with the y/rows/pitch values this is one consistent eax<->ecx swap
    of the row-loop pieces. 48 random combinations of 11 neutral spelling sites (round 323) either keep +0x187 or
    break the matched prologue (+0x0/+0x20).
    Rounds 324-330 - piece-to-block logger (autoglob.cdb G lines: id/priority/register/cost/allowed set per global
    pick; autopiece.cdb P lines: first source line of each block a candidate is live in). The list is sorted by
    priority (+0x0c) descending, ties by +0x40 descending; +0x40 is the index of the LAST tuple referencing the
    candidate, counted in block-list order (FUN_1072cac2). In ours the skipped-row segments counter (pri 56, last
    tuple 0xf0) and the row-loop pitch temp (pri 56, last tuple 0xec) tie, segments goes first and takes eax, pitch
    gets ecx, and y/rows/height follow - the whole +0x187 swap. The original needs pitch first.
    Measured: `--rows == -1` drops pitch to 54; `rows-- <= 0`, `rows-- == 0`, `rows <= 0 break; rows--`,
    `rows--; if (rows < 0) break` change only the tie or lower pitch (round 329: 71 combinations of rows-check x
    y-check x skipped-row order x tail order; pitch first in none). if/else spellings give identical code (block
    order is canonical). `while (--rows >= 0 && y < height)` gives the original's registers (pitch eax, y/rows ecx)
    but moves the rows test before the y test, merges the y>=height check and changes stack slots (first
    difference 0x19) - not the original's control flow. Round 330: an inline skipRow helper taking `BYTE*&` gives
    code identical to the base; one returning the pointer breaks the prologue (+0x20).
    Rounds 331-337 - the row loop as `if (y < height) { do { ... } while (y < height); }` is the first spelling
    that puts the pitch value first (priority 59 vs the skipped-row segments counter 56; pitch eax, segments ecx,
    the original's row-loop registers; multiset 56 -> 22). NOT usable: with the condition at the bottom the
    compiler proves y < height at the top of the body and drops the `y >= height` half of the skipped-row test
    (one compare and branch fewer than the original), which also changes the frame (first difference 0x19) and
    the top-skip loop (rows in ebp, y on the stack). The original was a plain `while`: VC6 rotates it after the
    range optimisation, so the original keeps both compares. 6 top-skip spellings, 4 `line` placements, 40
    neutral-spelling combinations, 40 prologue orders and 7 lea/condition spellings on top of the do-while form
    give nothing better (rounds 332-337). The skip-loop `lea edi,[edx+edi+1]` operand order (ours [edi+edx+1],
    also in the base file) does not move with any spelling of `src += count + 1` or the type of `count`.
    Frame layout (static reading of c2 FUN_1071fc89 / FUN_10749846): stack variables are kept in a list sorted by
    size, then by the number of memory references (more references -> earlier, lower slot), ties by first
    reference; slots are then packed in that order. A variable that loses one memory reference can move slots.
    Rounds 338-341 - per-block priority logger (Probe\weights\autoprio.cdb, breakpoints on the three priority
    updates of c2 FUN_10722463 at 0x10722d4c / 0x10722d6b / 0x10722d99; "Q k= id= P= b= blk= line=" lines;
    summary tool search/qprio.py). The sums reproduce every logged priority exactly. Per block, P = (number of
    candidates referenced in the block) * 2^loop depth; a referenced candidate gains P * its benefit (1 or 2 per
    reference), a live unreferenced one loses P. Base file: pitch temp = +28 (line setup) +32 (row tail)
    +24 (skipped-row entry block, P=12, b=2) -28 (live in the loop test, rows check, both y-range compares, the
    skipped-row loop and the bottom test) = 56; skipped-row segments counter = +48 (same entry block, b=4) +8
    = 56. Pitch needs +1 (or the entry block one candidate fewer: pitch 52, segments 48). The do-while form gains
    pitch +3 only because the dropped `y >= height` compare block no longer costs it 4.
    The front end normalises expressions: 18 probes (skipped-row skip spellings `*++src`, `src[1]`, no count, BYTE /
    unsigned count, `src++; count = *src++; src += count`, separate segments declaration, tail order, `line =
    line + ...`, named surface / offset / rowOffset / xOffset temporaries for the line setup) reach c2 with
    identical candidates and priorities (only line numbers differ; the tail order moves pitch's tie 0xec -> 0xeb).
    Only control structure reaches the allocator. Rich header: all 290 C++ objects of zoo.exe are c2 8447 (ours).
    Rounds 342-344 - inline helper splits, scored with the priority logger: a row drawer taking `BYTE*& src`
    (alone, with a pixel blender, with skipRow(BYTE*&) on one or both skip loops), a pixel blender alone, skipRow
    on both loops, a GXCanvas pitch accessor (free inline, const and non-const, at 1-3 sites) and the skipped row
    as an if/else either way round: all reach c2 with the base file's candidates and priorities (pitch 56,
    segments 56) and give the base code - c2 inlines them before allocation and the copies vanish. The one
    exception is a row drawer that takes src by value and returns it (`src = drawRow(...)`): its return copy
    lands in the row tail block (P 8 -> 12), pitch rises to 72 and takes eax with segments ecx (the original's
    row loop), but src becomes two webs (src 246, esi) and the whole allocation moves (first difference +0x8,
    multiset 154). So the original's row tail references the same four candidates as ours; nothing found
    adds one without splitting src.
    Rounds 345-346 - the 24-bit twin GXLLE::drawDitherMirror24 (0x472A25, `#line 668`), rebuilt from the current
    32-bit source minus the alpha byte (walking `*d++` or `dst[0..2]` writes: identical code), now matches its
    original up to +0x187 exactly like the 32-bit function (rounds 266-267, on the old source, differed early).
    Its 40 remaining differences are the same row-loop eax<->ecx swap and the same skip-loop lea operand order,
    and the logger shows the same tie (pitch 56, skipped-row segments 56). Its original keeps pitch in eax and
    the segments counter in ecx too. So two functions share one source shape and one wall; the twin shows no
    construct we lack. Macro-style `do { } while (0)` wrappers (fakematch tricks, used only as probes) around
    the skip loops, the skipped row's `line += / y++` and the row tail all fold away: base priorities.
    The twin's source is not in Src (it would be a second mismatch at the same wall): the user's call.
    Rounds 348-350 - per-file flags and header types for gxlledither.cpp (both dither functions).
    Flags added to /O2 (Var_*.cpp.flags): /Op /Ot /Ox /Oi- /Ob1 /Ob2 /G3 /G4 /G5 /GB /GF /Gf /Gs /Gs4096 /Gy
    give byte-identical code (both stop at +0x187). /G6 (+0x7), /Oa, /Ow, /Ox /Oa, /Ox /Ow, /Oa /Ow, /O2 /Oa /Ob1,
    /G6 /Oa (+0x0), /Ob0 (+0x96, callees out of line), /Oy-, /O1, /Os, /Og- (+0x0, far worse) all move away. So the
    original file was built with the project's plain /O2. Header types: DDSURFACEDESC2 with lPitch outside its
    union, as int, as DWORD, or dwHeight/dwWidth as LONG (a modified bfddraw.h copy inside the probe) give
    identical code and the same 56/56 tie. Neither flags nor these header types are the missing input.
    Rounds 351-358 - BLOCK ORDER, and the +0x187 wall solved. Probe\weights\blkdump.bat (+ autoblk.cdb,
    autosucc.cdb) dumps c2's block list per pass. The list is built in source order (skipped row before the row
    tail); the flow-graph pass FUN_1070acba -> FUN_1071437b rebuilds it in REVERSE POSTORDER of the depth-first
    walk FUN_1070a561, which visits each block's successors in list order [jump target, fall-through]. So the
    successor the walk enters first ends up LATER in the block list. `if (y < 0 || y >= height)` lowers to a
    first test whose jump target is the skipped row, so the skipped row lands after the tail, the segments
    counter's last reference (0xf0) comes after pitch's (0xec) and segments wins the 56/56 tie. Condition
    spellings (`!(y >= 0 && y < height)`, `0 <= y`, ...) are normalised by c1 to the same graph. A named bool,
    `bool outside = y < 0 || y >= height; if (outside)`, gives c2 a different graph (the bool is materialised,
    then folded back into the same two compares): pitch now goes first, and BOTH dither functions match up to
    +0x1e6 / +0x1ee. Promoted (round 358). What remains in each function: the two skip loops' lea operand
    order (original `lea edi,[edx+edi+1]`, ours `[edi+edx+1]`, same registers) - 2 instructions per function.
    Not moved by: 10 spellings of `src += count + 1` (incl. no count, BYTE/unsigned count, `&src[...]`),
    `count` declared at function scope before / after src (rounds 358-359).
73. **The skip-loop lea operand order (rounds 363-377, 2026-11-05).**
    - Whole-exe scan: the five-instruction skip loop (`inc p; xor c,c; dec n; mov cl,[p]; lea p,[..+1]`) occurs
      ~120 times. In the original the count is the base (`[cnt+ptr+1]`) for every count-in-edx loop whose pointer is
      in eax/ecx/edi (26/26) and for every ebp pointer; with the count in ecx/ebx/eax, or the pointer in esi/ebx, the
      pointer is the base. Our builds never give count-first except with an ebp pointer.
    - Test bed: a replica of 0x4F493B (the 378-byte GXLLE 16-bit mirrored draw, no lock), probe Var_m16 - same
      registers, same skip loop, nearly identical code; only the lea order differs (ours `[eax+edx+1]`, original
      `[edx+eax+1]`). ~70 skip-step spellings in it (casts to int/DWORD, operand orders, &src[], late constants
      via an `int one = 1`, reference / pointer-to-pointer / value-returning helpers, function-scope multi-use
      count, copies) give only TWO outcomes: (a) separate `inc` + pointer-first (every in-place `src` update), or
      (b) the increment folded into the load (`mov dl,[eax+1]; lea eax,[edx+eax+2]`) + count-first, whenever the
      count is read through a copy of the pointer. The original's combination (separate inc + count-first) never.
    - c2 internals (probes amdump/adddump/bothdump.bat, autoam/autoadd.cdb): address operands are built by
      FUN_1071f60f / FUN_107216d8 (base = operand +0x28, index = +0x2c), from the matcher FUN_10729327/
      FUN_10729864, which walks the ADD (0x16d) chain and puts the ADD's FIRST operand in the base. In-place
      `src += count + 1` reaches it as ADD(src, ADD(count, 1)) -> base src; the copy form as
      ADD(ADD(count, next), 1) -> base count (c2 put count before next). A post-RA fixup (FUN_10735ee8, tuple
      0x14d) swaps base/index when the base got ebp and the scale is 1 - the ebp cases above.
    - So the original's IL had the count first in that ADD while still updating src in place. Not yet found which
      source form or c2 rule produces that; next step is the pass that orders ADD operand lists.
74. **Where c2 fixes the order: the `x = x + rest` rewrite (rounds 379-384, 2026-11-05).**
    - c2's heap is deterministic for the same input, so hardware write breakpoints on a tuple seen in one run
      work in the next (Probe\weights\watchdump.bat + watch.txt, up to 4 addresses).
    - The skip-loop ADD(src, ADD(count, 1)) is built by FUN_1072735c (call at 0x107274c6 -> FUN_10721a1a):
      for an assignment `x = t` whose temp t is an ADD/SUB tree, FUN_10730671 searches the tree (descending only
      into compiler temps, sym kind 3, whose def has the same op) for an operand equal to x with the same type
      field; if found it rebuilds the statement as `x = x + (rest)`, x FIRST. The address matcher then makes x the
      base. bothdump.bat now logs every rewrite as "RW line= dest=".
    - With no rewrite (the dest not found in the tree) the ADD keeps count first: x4 / y0 / y6-y9 forms, where the
      new pointer comes from a user-variable copy (`BYTE* next = src; ... src = next + count + 1;`). But in all of
      them c2 also folds the separate increment into the addresses (`mov dl,[eax+1]; lea eax,[edx+eax+2]`).
    - Tried without the rewrite AND with the inc kept: none yet. Casts to DWORD/unsigned/long do not stop the match
      (types identical after c1); a copy used once is propagated (rewrite again); copies used twice either fold the
      inc or get rewritten themselves. ~100 skip-step forms in the 0x4F493B replica so far.
    - Next session: find how the original keeps both, i.e. what stops FUN_10730671 from finding src while the
      `inc` survives. Ideas not yet tried: the increment and the add in different basic blocks or statements that
      c2 cannot merge (e.g. the inc as the segment loop's step, `for (...; segments--, src++)`), src reached through
      a different symbol in the tree (a second pointer variable kept live across the loop), a SUB form
      (`src -= -count - 1`) that the search only follows on its first operand, and logging FUN_10730671's
      compare (FUN_10702b3c) for the original-like forms.
    Rounds 386-390 (same replica): SUB spellings (`src -= -count - 1`, `src - (-1 - count)`), the increment as the
    loop step (`segments--, src++`), `&src[count] + 1`, function-scope / loop-carried / twice-assigned copy
    pointers, a statement between `next = ...` and `src = next`, and the two-statement `src += count; src++;`
    all give the same two outcomes. bothdump.bat's E/F/RW lines show why: every form that keeps the `inc` reaches
    FUN_1072735c as `src = <tree containing src>` (F=1, rewritten src-first); a single-use copy is propagated
    away first, and `src += count; src++;` is already one ADD(src, ADD(count, 1)) by then (merged earlier). F=0
    only happens with a copy that survives (x4), and then the increment is folded too.
    Open hypothesis: the original's register-dependent pattern (count-first only with edx counts) looks like a
    post-allocation choice, e.g. a peephole fusing `add r,cnt` + `inc r` into one lea with its own operand order,
    which our IL never reaches because c2 merges the two adds earlier. Next: find that merge (the pass before
    FUN_1072735c that joins `src += count; src++`) and any post-RA add/inc -> lea peephole.
    Rounds 392-393: inline / static helpers taking the pointer by value after an in-place `src++`
    (`src = skipData(src)`, `skipData(++src)`, `skipData(src + 1)`) and, in gxlledither.cpp itself, a
    function-scope `BYTE* next` shared by both skip loops (assigned in both, so multi-def) - all still give either
    the rewrite (pointer-first) or the folded increment (`mov dl,[edi+1]; lea edi,[edx+edi+2]`). The folding is
    not about the copy having a single definition: c2 folds `src + 1` into the copy whenever src's incremented
    value has no other use.
75. **The full chain for the skip-loop lea (rounds 395-401, 2026-11-05; probe autorw.cdb in bothdump.bat).**
    - Before the rewrite the IL already has the count FIRST: for `src++; int count = *src; src += count + 1;`
      FUN_1072735c sees `src = t41`, t41 = ADD(t158, 1), t158 = ADD(count, src). Only the `x = x + rest` rewrite
      (FUN_10730671 finds src in the tree, F=1) turns it into ADD(src, ADD(count, 1)) -> base src.
    - The rewrite is skipped only if src is not in the tree. Every way of getting the pointer into the tree under
      another name fails at an earlier, local copy/value pass (FUN_1070d818 and its callers; watchdump on the x4
      copy tuple: its operand is replaced at the line of `next = src` by the temp of `src + 1`):
      a copy `p = src` taken while src is current is replaced by src (rewrite again, pointer-first); a copy that
      is the only use of the incremented src absorbs the increment (`p = src + 1`, src++ deleted) and the inc is
      folded into the addresses. The in-place `inc` survives only when the incremented src itself has two uses,
      which puts src in the tree.
    - Also tried here: `register` / `const` / `unsigned char*` src, a function-scope copy assigned in both skip
      loops of gxlledither.cpp (cp1-cp3: unchanged, pointer-first), the copy in the for-step (`segments--, src =
      next`: merged, pointer-first).
    - Conclusion so far: with this c2 every source form tried reaches one of the two outcomes; the original's
      combination needs the pointer in the add under a different symbol while the in-place increment stays, which
      c2's local copy propagation prevents in every form found. No source change promoted.
76. **Option 2: the five skip loops of 0x4FAECF (round 404, 2026-11-05).** In the original, the generic zoomed
    dither draw 0x4FAECF has five skip loops: the zoom==2 odd-offset row (pointer-first, count ecx), the top-skip
    rows (pointer-first, ebx), the drawn row's extra zoom rows (COUNT-first, edx), the skipped row's first row
    (pointer-first, ecx, src rebuilt from a `row` copy: `lea edi,[ecx+1]`) and its extra zoom rows (COUNT-first,
    edx). A skeleton with all five loops in that structure (probe Var_zf) compiles all five pointer-first
    (esi/edx, esi/ebx, esi/ecx). So with this c2 the order is not set by the surrounding code; the original's
    count-first loops must differ in their own statements, in a way no form tried so far reproduces. Types are not
    the lever either: autorw.cdb now prints operand types, and `(DWORD)src` arithmetic reaches the rewrite with the
    same type (0x1004) as the pointer.
77. **Intermediate-code edit reproduces the original exactly (rounds 406-408, 2026-11-05). ANALYSIS ONLY.**
    Probe\weights\norwdump.bat runs c2 under cdb and, for the statements selected in norw.txt, sets eax = 0 after
    FUN_10730671 returns (0x10727497), i.e. tells FUN_1072735c that the assigned pointer is not in the tree, so
    the `x = x + rest` rewrite is skipped and the IL stays `src = (count + src) + 1`.
    - 0x4F493B replica (statement offset 18): `inc eax; xor edx,edx; dec ecx; mov dl,[eax]; lea eax,[edx+eax+1]`,
      the original's sequence, increment kept.
    - The real gxlledither.cpp (current source, unchanged), with the rewrite suppressed at its four skip-loop
      statements (c2 line offsets 676, 695, 35, 54): compare.py "matched 6 | mismatched 0" - drawDitherMirror24
      and drawDitherMirror32 both match byte for byte.
    So the original was compiled by this c2, and the ONLY difference is that the skip statements' IL did not go
    through the rewrite: FUN_10730671 did not find src in the tree, or FUN_1072735c returned before searching.
    The search finds the assigned variable only as a direct operand of ADD/SUB nodes, descending only through
    compiler temps whose definition has two operands, and only with an exactly equal type field (+0xa) and an
    equal operand (FUN_10702b3c: kind, type, symbol). The source form that escapes it is the remaining target.
78. **A source form without the rewrite (rounds 411-414, 2026-11-05).** Operands of user variables compare by
    symbol (operand +0x14; +0x18 is a shared class record 0x107ae040), so the search can only miss src if the
    pointer in the tree is another symbol. Form found (probe Var_m16h, h1):
        int segments = *src++;
        BYTE* next = src;
        for (; segments != 0; segments--)
        {
            src++;
            int count = *src;
            next = src + count + 1;   // dest next: src is not the destination, no rewrite, count first
            src = next;               // copy; its source is a variable defined by a copy, so no rewrite
        }
        src = next;                   // second use keeps next alive (a single-use next is propagated away)
    In the 0x4F493B replica this differs from the plain form ONLY in the lea, now `lea eax,[edx+eax+1]` with the
    separate `inc` - the original's loop. In gxlledither.cpp (Var_h1d, Var_v1-v5: per-loop or function-scope
    next, const next, while form) the extra candidate `next` disturbs the allocation: drawDitherMirror24 differs
    from +0x13, drawDitherMirror32 from +0x187 (the old pitch/segments tie). The IL edit (note 77) matched with no
    extra variable, so the original's form most likely adds no register candidate. Not promoted.
79. **Automated sweep (rounds 419-421, 2026-11-05).** 567 skip-step forms in the 0x4F493B replica, checked
    automatically for "separate inc + count-first lea" (scratchpad sweep_an.py):
    - Var_sweep (339): 6 increment spellings x 25 add spellings x int count, plus 7 count types x 25 adds, plus
      15 forms without a count variable.
    - Var_sweep2 (205): 5 pointer types (BYTE*, const BYTE*, unsigned char*, ...) x 9 segment-loop shapes (for,
      while(segments--), counted up, unsigned counter, ...) x 5 statement forms.
    - Var_sweep3 (23): odd lvalues and comma/conditional forms (`*&src +=`, `(true ? src : src) +=`,
      `++src += *src + 1`, `(&src)[0] +=`, a `BYTE**` alias, `(void*)` casts, `count ? ... : ...`).
    Result: 566 pointer-first with the inc, 1 count-first with the inc folded (the copy `s`), 1 different (the
    conditional). None reproduces the original. With the same variables and references as our source (which the
    IL edit shows the original has), no spelling found escapes c2's `x = x + rest` rewrite.
80. **Lead 1: copies removed after the rewrite (rounds 423-424, 2026-11-05).** Probe deldump.bat logs every
    tuple unlinked (FUN_1070179c) between the rewrite pass and the first priority computation. For the h1 form the
    only copy removed is one x86 `mov src, next`, by FUN_1072df43 (ret 0x1072e133): it merges a move into the
    IMMEDIATELY PRECEDING definition of its source (`next = lea ...; src = next` -> `src = lea ...`). Nothing else
    removes copies there. So a second pointer can only vanish before allocation if all its uses are such adjacent
    moves; but a pointer whose only use is that adjacent copy is already propagated away by the earlier
    block-local value numbering, before the rewrite check (x1/x3/x4: next initialised or not, no use after the
    loop -> next gone early, rewrite, pointer-first; allocation otherwise unchanged). With a second use (h1) it
    survives to allocation and shifts it. Lead 1 is closed: no copy both survives to the rewrite check and is gone
    before register priorities.
81. **Lead 2: the front end's intermediate code (rounds 426-429, 2026-11-05..10).** Probe ildump2.bat
    (autoil2.cdb) prints each function's IL as c2 reads it from c1xx (after FUN_1071b973). Variables arrive as
    kind-2 operands; `src += count + 1` arrives as `t1 = count + 1; t2 = src + t1; src = t2`, and c2 itself
    regroups it into (count + src) + 1 before the rewrite. All 567 sweep forms give 73 distinct skip-loop IL
    shapes; none has a temporary copy of src. A last batch (Var_sweep4: inline functions returning a reference or
    a value, `BYTE* const&` parameters, a static member helper, conditional expressions, int/DWORD round-trip
    casts) shows inline calls arriving as call temps (ops 0x15a/0x184), but c2 expands them before the rewrite,
    so all came out pointer-first (one conditional form changed the code). Lead 2 closed: no construct found makes
    this front end hand c2 the pointer in a form its search misses.
82. **MSVC6-decomp / MSVC6-tooling cross-check (round 431, 2026-11-10).** The SMSG-decomp research repos
    (github.com/SMSG-decomp/MSVC6-decomp, a Ghidra decompilation of VC6 RTM 8168 with recovered names, and
    MSVC6-tooling, Rust diff tools + probes) name our functions: FUN_1072735c = form_read_modify_write,
    FUN_10730671 = find_rmw_dest_in_expr, FUN_10702b3c = operand_compare. Their code agrees with our reading of
    8447 exactly, and closes the remaining loopholes:
    - pass_form_read_modify_write runs unconditionally under /Og, right after pass_mark_register_candidates. The
      rewrite is skipped only for float stores (type 0x4xxx), a top op outside add/sub/and/or/xor/shift, or the
      dest not found (exact type, kind, then symbol).
    - Kind 2 -> 1 marking depends on the symbol (storage flags, class) and type, not on the occurrence, except the
      first operand of a call tuple (kind 0x0e). Operand flag 0x40 (which blocks marking) is only set by the
      interlocked intrinsics and longjmp unwinding. So there is no natural per-occurrence kind mismatch.
    - The inliner (runs first) gives a formal that the inlinee writes its own cls-4 local and folds the return copy
      into the caller's variable. Tested (Var_svh, 10 helpers like `inline BYTE* skipSegment(BYTE* p) { p++; int
      count = *p; return p + count + 1; }` with `src = skipSegment(src);`): 8 count-first but with the increment
      folded (`lea eax,[edx+eax+2]`), the same outcome (b) as user copies, 1 pointer-first, 1 a real call (static).
    - MSVC6-tooling has no probe on this; its commswap diff only classifies lea operand swaps ("hash" when both
      operands are leaves, else "depth/size"), it does not explain them.
    Still open, still not promoted.
83. **Other VC6 decomps (2026-11-10): CMR2Decomp, homm3-decomp, snail, toy2-pc-decomp, motocross-madness-2-decomp.**
    None of them describes form_read_modify_write or has an RLE skip loop like ours. What carries over:
    - snail (tools/match/c2/address-order.md, same c2 family): c2 sorts the operands of every commutative node by a
      packed cost, descending, in the early expression passes; the first becomes the SIB base. For two symbols the
      cost is `0x10000 | hash`: a local or parameter hashes `id << 5`, with ids handed out in the order the IL
      meets the symbols (first 31 locals take ids 1-31); a compiler temp hashes `(id mod 1024) << 6`. This is why
      the unrewritten IL reads (count + src): count is met later, so it hashes higher. Our rewrite runs AFTER this
      sort and puts the destination first, so nothing re-sorts it.
    - homm3-decomp (docs/vc6/regalloc.md 6b) and motocross (docs/VC6_OPERAND_ORDER.md): the same order rule seen
      from the source side ("the operand born later takes the base"; "the newer leaf loads first"), with levers
      such as hoisting an initialiser or giving a loop its own index. They only move adds that are NOT rewritten,
      so they cannot reach the skip statement while the rewrite fires.
    - snail also confirms that a by-value pointer parameter of an inline helper becomes an inline-copy local with a
      late id (our note 82 result).
    No new lever for the skip statement; the open problem is still escaping the rewrite without the increment
    folding.
84. **The escape form in gxlledither.cpp, loop by loop (rounds 434-440, 2026-11-10).** compare.py with drawDitherMirror24
    added to the map (local copy: `drawDitherMirror24@ = 0x472A25`).
    - The note-78 form (`int segments = *src++; BYTE* next = src; for (...) { src++; int count = *src;
      next = src + count + 1; src = next; } src = next;`) in all four skip loops: every skip-loop lea is now the
      original's `lea edi,[edx+edi+1]`, and drawDitherMirror32 differs ONLY by the old +0x187 eax<->ecx swap (pitch
      vs y / rows / segments temps); drawDitherMirror24 also swaps esi/edi from +0x13.
    - The same form in the top-skip loops only (Var_m1): drawDitherMirror32 is exact except the off-screen row's lea
      at +0x1ee. So the top-skip loop is solved by this form; the off-screen row is what brings back +0x187.
    - Priority dump (autodump, p_wbase/p_wtop/p_wh1/p_wk7): the +0x187 tie is the pitch temp (56) against the
      off-screen row's segments counter (56); pitch wins on the tie field, as round 358 found. With `next` in the
      off-screen row the segments counter rises to 64 (next adds pressure to that loop's blocks) and pitch drops to
      52-56, so the counter takes eax first. With next only in the top-skip loop both stay at 56.
    - Tried in the off-screen row (all stop at +0x187): 36 combinations of line/y order, four ways of writing next
      (next first or src first, `src = next + 1`), for / while(segments--) / while with a decrement, next
      assigned before or after the line/y updates (Var_q00-q35); a guarded do-while; segments read before the line
      update; 6 spellings of the `outside` test (named bool, inside, const, no bool, before the rows check) on two
      of these forms (Var_r*); function-scope next at 3 positions, with and without the `outside` bool.
    - drawDitherMirror24: the +0x13 esi/edi swap goes away when the off-screen row reads segments through next
      (`BYTE* next = src; int segments = *next++;`), leaving the same +0x187 swap.
    - The original keeps nothing extra in the off-screen row (segments ecx, count edx, src edi), so its source most
      likely has no second pointer live in that loop. Open: a form that escapes the rewrite there without a live
      second pointer, or one that also raises pitch's priority. Not promoted.
85. **Last two levers on the +0x187 tie with the escape form (round 442, 2026-11-10).**
    - Per-block priorities (qp2.py on p_wk7): the off-screen row's entry block goes from P=12 to P=14 with `next`
      in it; the segments counter gains 4 per P (b=4), the pitch temp 2 (b=2): counter 64, pitch 56.
    - Option 1, a named `int pitch = canvas->mDesc.lPitch;` (and `const int`) after the lock, before `line`
      (Var_p3/p5): pitch gets a stack slot, frame +4 (`sub esp,0x28`), first difference +0x0. Earlier positions
      would read lPitch before lockWrite() fills it and were not built.
    - Option 2, `next` created only inside a loop guarded by `if (segments != 0)` (do-while or for; with the top-skip
      loop in the note-78 or the guarded form; Var_v1-v6): every variant still stops at +0x187, drawDitherMirror24
      too when the top-skip loop uses the guarded form.
    Both options closed. The dither pair stays a documented mismatch (2 instructions each, source unchanged).
86. **Option 4 promoted, option 3 measured (rounds 444-445, 2026-11-10).**
    - PROMOTED (round 445): drawDitherMirror32's top-skip loop now uses the second-pointer form
      (`int segments = *src++; BYTE* next = src; for (; segments != 0; segments--) { src++; int count = *src;
      next = src + count + 1; src = next; } src = next;`). Main build: drawDitherMirror32 differs ONLY by the
      off-screen row's `lea edi,[edx+edi+1]` at +0x1ee (1 instruction); nothing else moved. drawDitherMirror24
      keeps the plain form (the same change there swaps esi/edi from +0x13) and its 2 lea instructions.
    - Option 3 (off-screen row without the extra pressure), priority dump p_wv3/p_wv4: with `next` created only
      inside a loop guarded by `if (segments != 0)` and `src = next` after it (for form, Var_v4), the entry block
      is back to P=12 and the segments counter to 56; the only cost left is the post-loop `src = next` block
      (P=2, pitch -2): pitch 54 vs counter 56, still the counter first (+0x187). The do-while form is worse
      (counter 64, pitch 58). The second use of `next` that keeps it alive past value numbering always lands in a
      block where pitch is live but unreferenced; no form found that puts it in an existing block.
87. **Both dither functions down to 1 instruction (rounds 448-450, 2026-11-10).** drawDitherMirror24's top-skip loop
    in 8 spellings (off-screen row and drawDitherMirror32 unchanged): the guarded form
        int segments = *src++;
        if (segments != 0)
        {
            BYTE* next;
            for (; segments != 0; segments--)
            {
                src++;
                int count = *src;
                next = src + count + 1;
                src = next;
            }
            src = next;
        }
    (and the same with a do-while, identical code) changes ONLY that loop's lea to the original's
    `lea edi,[edx+edi+1]`. The unguarded second-pointer form swaps esi/edi from +0x13 there; reading segments
    through next (k3/k6/k7) folds the increment (`mov dl,[edi+1]; lea edi,[edx+edi+2]`); `next = src + 1`
    before the loop changes the loop. drawDitherMirror32 compiles identically with the guarded form, so both
    top-skip loops now use it (round 450). Left in each function: the off-screen row's skip-loop lea (+0x1e6 /
    +0x1ee). The guarded form in the off-screen row brings back +0x187 (note 86: pitch 54 vs segments 56).
88. **Last batch on the off-screen row (round 452, 2026-11-10), on the round-450 source.** All 10 fail:
    - segments counter live after the copy (exit `if (--segments == 0) break;` after `src = next`,
      `while (segments-- > 0)`, decrement after the copy in a do-while; Var_xa2/a5/a6): +0x187 in both functions.
    - guarded, next initialised inside the guard and copied back at the loop top (do / for / while, and the
      `src = next + 1` spelling; Var_xb1-b4): drawDitherMirror24 +0x187, drawDitherMirror32 +0x20 (prologue).
    - if/else instead of `continue` (drawn row in the else branch with its own line/y tail; Var_xc0-c2): the plain
      skip gives code identical to the current source (control); guarded +0x187, unguarded +0x13 / +0x187.
    The off-screen row's lea stays the one open instruction in each dither function.
89. **Option 2: other count-first skip loops in zoo.exe (2026-11-10, static scan of the whole image).** 125 skip loops
    of the form `inc p; xor c,c; dec n; mov cl,[p]; lea p,[..+1]` (scratchpad skiploops.txt):
    - count-first (original's `[cnt+ptr+1]`): 26, ALL with the count in edx and the pointer in eax, ecx or edi;
    - pointer-first: 99. Of these, 21 have the count in edx too, but then the pointer is ALWAYS esi or ebx
      (19 esi, 2 ebx); none has an eax/ecx/edi pointer with an edx count.
    - The count-first loops are all in the GXLLE draw family (hot copies 0x416B06, 0x480C3E, 0x4812BF, 0x48D978,
      0x48DF66, 0x4997E1, 0x4EEA54, 0x4EED12, 0x4FEB72, 0x505F13, 0x50616C, 0x52EA00 and the cold 0x5F0xxx-0x5F3xxx
      blocks). Their surroundings are the same row/segment structure as ours; the same loop shape (segments
      counter in eax, count edx) also appears pointer-first with an esi pointer in the same family
      (0x4EF093 next to the count-first 0x4EEA54). No member has a simpler or distinctive skip spelling to copy.
    - The split follows the pointer's REGISTER across all 125 loops, which a pre-allocation choice (the rewrite)
      would not obviously produce. Open question, not resolved: in which way the esi/ebx-pointer functions
      differ from the eax/ecx/edi ones before register allocation. Answering it needs one pointer-first sibling
      and one count-first sibling decompiled far enough to compare. No source change.
90. **Sibling comparison: the rewrite ran in one twin and not the other (rounds 455-458, 2026-11-11).** The
    renderer dispatcher calls plain/mirrored pairs; for zoom 1, 16-bit: 0x4F47AA (plain, top-skip loop
    pointer-first, `lea esi,[esi+ecx+1]`) and 0x4F493B (mirrored, count-first, `lea eax,[edx+eax+1]`). Both written
    as members of a scratch struct with the SAME skip spelling (`src++; int count = *src; src += count + 1;`);
    both are close to the original (only the prologue's load order differs).
    - Normal build: 0x4F47AA's skip loop is the original's exactly (esi/ecx, pointer first, rewrite applied);
      0x4F493B has the original's registers (eax/edx) but pointer first.
    - norwdump (Tools\vc6probe, rewrite suppressed only at the skip statement, line 18 of each): 0x4F493B becomes
      the original's `lea eax,[edx+eax+1]`; 0x4F47AA becomes `lea esi,[ecx+esi+1]` (registers unchanged, now WRONG
      order). Before the rewrite both statements are the same tree, (count + src) + 1 with count first.
    - So in the original the rewrite ran in 0x4F47AA and was skipped in 0x4F493B, and the registers come out the
      same either way: the count-in-edx correlation of note 89 is a family coincidence, not the cause. With one
      spelling our compiler gives one twin right and the other wrong, so the original's two twins must spell their
      top-skip statement differently (or differ in something the rewrite reads). The count-first spelling is
      still unknown; it is used in the mirrored / zoomed draws and in some loops of the mixed functions (0x505FED,
      0x4FAECF), not in the plain ones.

91. **A caller's `test al,al` after a virtual call means the callee returns bool (rounds 465-472, 2026-11-11).** When the
    caller tests the result with `test al,al`, the callee's declared return type is `bool` even if its body returns
    through `mov eax,1` / `xor eax,eax`. DX8SndMgr::isValid (slot 11, 0x404A7E) and SNDSoundResource::isValid were
    declared `int` and every caller emitted `test eax,eax`; changing them to `bool` fixed DX8Sound::instantiate's
    +0x19 difference and kept all 46 other snd functions exact. Check the caller's test width before touching bodies.
    Related: getters that return `x ? x->f : 0` or MAKEWORD of header bytes must be declared `int`: the original is
    `mov eax,ecx`, a `WORD`/`BYTE` return gives `mov ax,cx` (GXImageTGA/BMP getWidth, getHeight, getDepth,
    getBitCount).
92. **Shared resource-load idiom wall (rounds 467-471, 2026-11-11).** GXImageTGA::attempt (0x4B32A7) and
    GXImageBMP::attempt (0x5234DA) both read the file data as `handle.mEntry ? handle.mEntry->mData : 0` and
    then use the result twice. The original copies the pointer to a second register before adding the header
    size (`mov ebx,[ebx+0xc]; mov ecx,ebx; add ebx,0x12` TGA, `mov edx,[ebx+0xc]; mov eax,edx; add edx,0xe` BMP).
    Tried and rejected: header pointer with `header+1` inline, separate `file`/`body` locals (prologue becomes
    `push ebp`), a BFResourceHandle::getData() inline (no change), and a front-to-back cursor (`cursor = data;
    hdr = (T*)cursor; cursor += sizeof(T)`): identical object for BMP, wrong prologue (`push ebp`) for TGA. The
    original's null path is a cold `xor edx,edx; jmp` block, so the ternary is right; only which variable owns
    the ternary's register differs. Both are permuter targets and share one fix.
93. **DX8Sound positioned play (rounds 476-479, 2026-11-11).** play / playLooped / updatePosition take a `BFPos*`
    (0x440764, 0x441797, 0x44153B) and call 0x43F5BA(pos, &volume, &pan) first. The sum is
    `getVolume() + mVolumeB + mVolumeA + volume`; each is exact except one load: the original reads mVolumeA
    into edi before mVolumeB (+0x46 / +0x27 / +0x4a). Reassociating (`volume + (...)`), `attenuation += volume` and
    A-before-B (`getVolume() + mVolumeA + mVolumeB + volume`) all leave our object byte-identical (each build
    checked against the committed file size), so the expression tree is not the input. Parked, permuter targets.
    DX8SndMgr::load / instantiateFor (slots 5 and 6, 0x61FF0A / 0x61FF20) are plain forwarders to the DX8Sound
    methods of the same name and match.
94. **Key-name matchers are `key == "literal"` (round 487, 2026-11-11).** ZTAIMgr vtable 0x63536C slots 10-12
    (0x4A9B8E / 0x4A9F0D / 0x4AA02F) return whether a `const std::string&` equals "fMoveSlow" / "fMoveMedium" /
    "fMoveFast": STLport `operator==(string, const char*)` compiles exactly to the original (size compare, cold
    `repz cmps`). About 80 more one-string functions of this shape sit in slot 10 of unnamed classes
    (bFix, bSick, bClean, ... in Notes\inventory.csv, strings column): they need their class names first.

95. **A tiny helper BBT pastes into callers must be defined out of line in some object of the batch (rounds 499-504, 2026-11-12).**
    UIControl::setFlag (0x4014AC) and its wrapper markClean (`setFlag(0x80, false)`, name: guess) have no standalone body in
    zoo.exe: BBT pasted them into every caller, a wrapper inside a wrapper giving the `sub esp,4 / push 0 / push 0x80 /
    sub esp,4 / cmp [esp+8],1` pattern of UIImageSet::vslot22/23. compare.py can only expand a pasted body when the callee
    is defined in our own objects, so both go out of line in uicontrol.cpp. Making setFlag a header inline (round 500) broke
    11 earlier UIControl matches (the compiler open-coded it); making only markClean out of line (round 504) fixed the nested case.
96. **Out-of-line copy constructors keep `new T(*this)` clones matching (round 503).** UIView::clone (0x60A8D2) and UIImageSet::clone
    (0x622FD7) call the separate copy constructors 0x620A90 / 0x622FF9; an implicit copy constructor is expanded inline by our
    compiler. Declare `T(const T& other);` without a body in the file with the clone and map the constructor. clone is slot 12
    (purecall in UIControl, non-pure here so the derived classes are not abstract).
97. **Override attribution (rounds 491-505).** An address found in a derived class's vtable slot is that class's override, not the base's:
    0x401302 is UIButton::vslot07; 0x4010E1 and 0x4435B9 belong to other vtables. Take the base slot from the base class's own
    vtable (UIControl 0x63203C), the override from the derived one (UIView 0x6314C8: 29 0x442493, 30 0x44361A, 31 0x4435B9).
98. **Scalar deleting destructors need only a map line when the destructor is implicit (rounds 505-506).** UIView ??_G 0x620A72 matched
    with `??_GUIView@@UAEPAXI@Z` in zoo.map. UIImageSet's deleting destructor 0x503054 has the destructor expanded inline
    (the vptr store is kept), which our compiler reproduces for an inline `virtual ~UIImageSet() {}` in the class.
    Destructors with real bodies (UIButton 0x4E0C63, UIEditableText 0x502ED5, UILayout 0x502353, UIScrollBar 0x502C45) are still open.
99. **Vtable 0x630C24 is GXImage, not UIControl (round 515).** Notes\classes.csv labels it UIControl; its slots are the forwarders
    0x4B3216 (calls slot 2), 0x4B3297 / 0x4B3287 / 0x61EF92 / 0x61EFA1 / 0x40D8BF (getWidth / getHeight / getDepth / vf8 / vf10)
    and 0x4B3685 (isValid), all reading the loader object at `this+4` (GXImageTGA / GXImageBMP, vtables 0x6351EC / 0x63585C), and 0x402876
    (release: virtual delete of that object, then null). Src\gx\gximage.cpp + Src\include\gximage.h match all eight. GXImage::isValid
    returns int (`mov eax,1`), not bool (`mov al,1`), although the inner call is tested with `test al,al`. The destructors 0x40D8EC / 0x40D952
    belong to derived classes (they store the GXImage vptr 0x630C24, inline release, then call 0x40D920 / 0x40D986 = vptr 0x635830):
    GXImage's own dtor/ctor are not standalone functions.
100. **Six `= 0` stores that compile as immediates are floats (round 513).** UIH_516C04 zeroes six globals; as `int` our compiler loads
    `xor eax,eax` once and stores eax, the original has six `mov dword ptr [g],0`: the globals are `float` (`= 0.0f`). When the original
    stores constant zero without a shared register, check for float before reordering statements.
101. **Entity hint timers (rounds 514-519).** f410f84 = `UIH_4017E5()->m_unk438`, the selected entity of the cached screen (0x1B58); an
    entity's `m_type` is at +0x128 and `m_type->isKindOf(&type_object)` is vtable slot 7 (+0x1C). Src\include\ztentity.h has both as real
    classes (vf0..vf6 placeholders). `ZTGame::contains` (0x443FFA, vector of entities at +0x80 of g_638040) is pasted by BBT into the
    5-second timers UIH_41A34C / 41A76F / 41A367, so it is defined out of line in Src\ui\ztgame.cpp (note 95). The 1-second timers
    41A3F3 / 41A733 / 41A413 and the "force" flag variants are plain functions; no macro is needed.
102. **UIListBox is the "UIBigCtl / UISelListCtl" of the old handler notes (round 520).** The method 0x4189E8 (index, scroll) writes +0x37C
    (selected index), counts +0x3C0 (the item list), calls 0x48BCE9 when the index is past the end, and scrolls (0x417695) or marks the
    control dirty. `UIListBox::setSelectedIndex` matches with `index >= (int)m_items.size()`. The class moved from uilistbox.cpp to
    Src\include\uilistbox.h. Still declared only: f48bce9, f417695, f4f9908 (remove item). Seven handlers use it (4CA58E, 47158C, 5B0199,
    4EE4C9 with a std::set, 4FA3A1, 501F2B).
103. **Iterator loops copy the original's increment order (round 522).** UIH_4EE4C9 walks a std::set and writes `++index, ++it`; its list twins
    (47158C, 5B0199) write `++it, ++index`. Mismatching that order shows up as one `inc edi` at +0x46.
104. **Mangled names of STL globals for symbols.map.** `list<ZTEntity*>`: `V?$list@PAUZTEntity@@V?$allocator@PAUZTEntity@@@_STL@@@_STL@@`;
    `set<ZTEntity*>`: `V?$set@PAUZTEntity@@U?$less@PAUZTEntity@@@_STL@@V?$allocator@PAUZTEntity@@@3@@_STL@@` (back-reference `3`).
    When unsure, `strings` the object file of the batch and copy the global's name from it. Tools\next.py ranks from the last committed
    zoo.map, so it keeps listing functions written in the current session.
105. **Pairs of `find(id)` blocks with setFlag (session 2).** `setFlag(0x10, on)` followed by `show()` / `hide()` on two controls (ids as pairs: 0xCBA/0xCBB,
    0x7D0/0x7D1, 0xE5C/0xE5D, 0x806/0x807, 0x7FE/0x82A) is 78 bytes per block in the original, the BBT-pasted `UIControl::setFlag`. Write `setFlag` before
    `show` / `hide`. These match only when `ui.uicontrol.obj` is scored in the same verdict run (otherwise they show as [outlined]).
106. **Tiny find-callers, shapes that matched:** `if (c) c->show()/hide()/vslot21()`; `if (c && (c->m_flags & 1)) c->hide()` (hide while shown); `if (c) c->vslot50(value, 0)`
    (value is the function argument, pushed after the 0); `find(id)` forwarded to the caller; show one control, hide another. Candidates are listed by scanning .text for
    `call 0x40157D` and normalising immediates; only about 17 shapes are left, all calling unknown non-virtual methods (OPEN_WALLS.md, 0x51A5EF family).
107. **GXImage (vtable 0x630C24)** is a forwarder to a loader object at +4 (GXImageSource, 11 slots); classes.csv labels it UIControl by mistake. `isValid` returns `int`
    (`mov eax,1`, not `mov al,1`). `ZTGame::contains` (0x443FFA) is pasted into the 5-second hint timers, so it must be in the same scored batch.
108. **A BBT-pasted wrapper shows as an extra `sub esp,4` before the pushes.** `UIStatusImage::vslot22/23` (0x4EF9F1 / 0x4EFA36) start `call base; mov ecx,esi; sub esp,4; push 0; push 0x80; sub esp,4; ...`:
    the first `sub esp,4` is the pasted `markClean()` (UIControl wrapper around `setFlag(0x80, false)`), the second is setFlag inside it. Written as `UIControl::vslot22(); markClean();`
    (UIImageSet does the same conditionally). `setFlag(0x80, false)` directly gives a different order and does not match. Both need `ui.uicontrol.obj` in the scored batch.
109. **`clone()` (slot 12) = `return new T(*this);`** with a declaration-only copy constructor; its address goes into zoo.map as `??0T@@QAE@ABV0@@Z` (the callee found in the
    clone body, also a vptr writer in classes.csv). Matched for UIStatusImage 0x6229DD, UIButton 0x4E99EE, UIGraph 0x623678, UIEditableText 0x620188, ZTMiniMap 0x6198D7 (allocation size
    = class size, which checks the declared layouts: 0x37C, 0x378, 0x3F4, 0x3AC, 0x3C0).
110. **Slot-40 forwarders** (UIButton 0x4F14E7, UIRadioSet 0x4F1515): `int result = 1; if (m_child) result = m_child->vslot40(a, b, c, d); return result;`. The early-return form
    (`if (m_child) return ...; return 1;`) compiles without the `mov eax,1` before the test and does not match. The child member is a `UIControl*` (+0x374 / +0xC4).
111. **UIManager methods called with `ecx = g_uiManager`:** 0x418F2F / 0x418F43 (cursor slots +0x50 / +0x54) and 0x4D5BEA (focus control's cursor, +0x10 / +0xA8) are UIManager members, not
    handlers. 0x443DD0 (`find(id)`, flag bit 3 test, then the event registry) is declared as `UIManager::f443dd0(int)`; its body needs the event registry class (OPEN_WALLS.md).

112. **Copy constructors: `: UIImage(other)` plus member copies.** UIView 0x620A90, UIImageSet and UIStatusImage match as a base-copy init list with the class's own members copied in the body
    (UIImageSet `m_current = other.m_current;`). The destructor `UIView::~UIView() {}` (0x502754) is an empty body. UIButton 0x4E9989 stays DIFF (attempt 2/2): ours writes the vptr first, the
    original after all member stores - lead: all 11 members (`m_unk365(other.m_unk365)`, `m_unk374(0)`) in the init list with an empty body (needs a budget extension).
113. **UIEditableText copy ctor wall:** the original inlines the string default ctor completely (three zero stores via esi, `push 8`, `call 0x40107f`); ours uses `lea edi,[esi+38Ch]` and a different register
    layout. This is the open alloc-proxy family (note 41). `m_text()` in the init list gives identical bytes. Attempt 2/2 used.
114. **Placeholder virtuals `vslot51()`..`vslot56(int)` in UIControl** shift nothing in the vtable and let overrides be written. Slot 55 is `_purecall` (0x629B58) in the 0x6313E4 class (abstract);
    overridden by UIView 0x620AA9 (a jmp), UIListBox 0x4EC999 (`f417a8e(true)`), UIStatusImage 0x4329C7, ZTMiniMap 0x490C95, UIImageSet 0x4DCA28, UIGraph 0x531D67, UIButton 0x41B26D.
    Slot 56 base 0x41BCE8 (one int argument): ZTMiniMap 0x4B2477 `m_unk394 = true; UIControl::vslot56(a);`.
115. **BBT block splitting:** UIStatusImage::vslot55 is a plain `if (m_unk4C > m_unk50) m_unkB0 = true; else m_unkB1 = true; f4328ae(m_unk36C, m_unk368);` - the duplicated tail call in the original
    is the post-link pass, not two source calls.
116. **ZT manager interface slots** (BFMgr-derived, vtable 0x6355C0 base): ZTScenarioMgr slots 3/4 (0x4C9BB2, 0x4B27E8) `if (m_unk30 != 0) { m_unk30 = 0; return true; } return false;`, slot 5 false,
    slot 11 `m_unk30 = 4`. ZTAdvTerrainMgr::f40dcb4 sets `m_unk08 = value; g_638064 = value > 0;`, vf1 calls it with 0 and returns true. Shared "return true/false" functions at one address
    (0x410CB0, 0x454E84, 0x40100B) serve many vtables and cannot be assigned to one class.
117. **Patching files from scripts:** anchor on a unique string or use `rindex`; `s.index('// 0x4E9989')` hit the class-declaration comment and truncated uibutton.cpp. Re-stage and verify after every force-commit.
118. **UIElement has six empty virtuals and NO destructor; the destructor is slot 6 of UIControl.** UIElement's vtable 0x632258 holds six pointers to 0x40100C (`ret`); UIControl's vtable
    0x63203C has them as slots 0-5 and the deleting destructor 0x4E0C83 as slot 6 (a `delete child` in the original is `call [vtable+0x18]` with `push 1`). Declaring `virtual ~UIElement();` made ~UIControl end
    with a call to a base destructor the original never makes; `virtual ~UIElement() {}` still emits that call. With six inline `vslotNN() {}` stubs in UIElement and no UIElement destructor,
    UIControl::~UIControl (0x4E0BC1) matches. The old header's slot numbers stay valid (offset = slot * 4); only the destructor moved from slot 0 to slot 6.
119. **Destructor bodies matched in this layout:** ~UIControl 0x4E0BC1 = `g_uiManager.f4e0b8a(this); f4b203f(0);` (UIManager::f4e0b8a 0x4E0B8A clears the manager slots +0x08/+0x10/+0x14/+0x18 that hold
    the control; f4b203f 0x4B203F = set parent, here 0). ~UILayout 0x502353 = `while (!m_children.empty()) { child = front(); child->f4b203f(0); delete child; }` (list of UIControl*, not void*).
    ~UIButton 0x4E0C63 = `if (m_unk374) m_unk374->f4e0d9a(this);` (f4e0d9a 0x4E0D9A is declared on UIControl as a placeholder; the real owner class is unknown). ~UIEditableText 0x502ED5 = `g_uiManager.f41ad6a(this);`
    plus the inline destructor of the std::string at +0x38C. Every one of them ends with the ~UIImage call (0x4E0996, still unwritten, 400+ bytes) that the compiler adds.
120. **Deleting-destructor wrappers with an inlined body** (UIImageSet 0x503054, UIStatusImage 0x502B10): the class has an empty (or member-only) inline destructor; the wrapper in the original contains
    it. Not separate functions. UIGraph 0x503382, UIScrollBar 0x502C45 and ZTMiniMap 0x5034B8 have real bodies that inline std::map / vector<part> teardown (open).
121. **UIControl slot 18 `show` in UILayout (0x443B70)**: forward to every child in the +0xB8 list (`(*it)->show()`), then `UIControl::show()` (0x4018C6). `hide` (0x4B1B86, slot 19) is different: it first builds a temporary list of the visible children (flag bit 4 test) and calls `hide` on those, then on the rest, then 0x41AC49 - open (STLport temporaries).
122. **UIScrollingRegion destructor 0x503003 = empty body**: the second base UIScrollable's vptr store (+0x35C, 0x635578), the `list<void*>` member at +0x39C (clear + header node returned to the STLport freelist 0x638004) and the tail call to ~UIImage are all implicit. The deleting wrapper 0x502FE5 matches with it. UIListBox's (0x502B6F) is not empty: it deletes the owned items of the list at +0x3C0 through their virtual destructor (slot 0, item class unknown), calls DeleteObject (GDI32) on the handle at +0x3B0, then tears down the vector at +0x3C4.
123. **Reference-counted resource handle (SND/GX)**: `BFResourceHandle::set` 0x407306 = `if (entry == mEntry) return; if (mEntry) mEntry->release(); mEntry = entry; if (entry) entry->addRef();`; `release` 0x407330 = `if (--refs == 0) freeData();` (freeData 0x402EC7); `reset()` is an inline `set(0)` (SNDSoundResource::vf4 0x4072FA only matches through it: the original adds 4 to `this` before pushing the 0). **addRef is an out-of-line function (0x4038F2, `inc [ecx]; ret`) that BBT pastes into the callers**: written inline VC6 gives `inc [esi]`, the original has `mov ecx,esi; inc [ecx]`. Other handle types (the one behind SNDSoundResourceWAV/GXImageTGA slot 4, 0x4072A3, which calls the copy 0x4072B9) have their own copies of set/release: the same source repeated per type, not one shared function.
124. **UIImage slots 18 / 19 (0x4018D5 / 0x41ACBB)**: the vtable 0x6313E4 row of classes.csv owns them (UIButton, UIView, UIScrollBar, ... inherit). `show` = `UIControl::show(); if (m_unk350 && m_unk174 != 0) { m_unk174->Release(); m_unk174 = 0; }` (+0x174 is a COM surface: `push eax; call [vtable+8]` is IUnknown::Release); it matches. `hide` remembers `m_unk350 && flag bit 0` in a byte local, calls UIControl::hide (0x41AC49) and then sets +0x34F when both held; two spellings left one difference: the original reads the flags with `mov al,[esi+0x7c]` (byte load) where ours loads the dword (`m_flags & 1`, `flagBit(0) == 1`) - the flags are probably tested through a BYTE-typed expression.
125. **UIImage slot 43 (0x41ADF1)**: timer countdown `if (flagBit(10) == 1 && (m_flags & 1) == 0)`: when `m_unkA0 == m_unkA4` decrement, else `m_unkA0 = m_unkA0 - now + g_638f7c` and `show()` when it reaches 0 (if the UI manager's m_unk0C is this, g_638f8c = 0). Body and flow match; only the prologue differs (extra `push edi`, shrink-wrap). Parked in OPEN_WALLS. Round 572 lesson: an extra `m_unkA8[4]` in UIControl grew every UI class by 4 bytes; check sizes after touching uicontrol.h.
126. **Reused out-parameter local (DX8Sound BFPos play / playLooped / updatePosition, 0x440764 / 0x441797 / 0x44153B)**: the original accumulates the volume in ONE local (`volume += g_sndMgr->getVolume() + mVolumeB + mVolumeA;`, `-volume` for the pan) where a separate `attenuation` local gave different registers. Same source variable, same register: when a sibling uses one local for two meanings, copy that.
127. **SNDSoundResource handle chain (0x4072FA / 0x41E5E3 / 0x61FFAF)**: `~SNDSoundResource() { vf4(); }`, `BFResourceHandle::~BFResourceHandle() { reset(); }`, `reset() { set(0); }` (reset is out-of-line, BBT pastes it). vf3 calls the handle method at 0x4047F4 (`f4047f4`, name unknown; NOT `load` 0x403891) and runs `attempt` only when ALL of entry / mUnknown4 / mUnknown8 / mData are non-null; otherwise it still succeeds. vf3 returns `int`: the callee's `mov eax,1` (not `mov al,1`) shows the return type, the converse of note 91 (a caller's `test al,al` means bool).
128. **DX8Sound::release (0x4029D5)**: two small out-of-line helpers (`releaseBuffer`: Release + null; `releaseResource`: delete + null, names guessed) pasted into release by BBT; written as non-inline member functions they match.
129. **`ret N` handlers that reload ecx are `__stdcall` free functions (UIH_506FC0 0x506FC0)**: a function that ends in `ret 8`, never reads `this`, and itself does `mov ecx,0x638de0; push id; call 0x40157D` is a free `__stdcall` function calling `g_uiManager.find(id)`. Written as `UIManager::method` it fails (the original has the extra `mov ecx,0x638de0`, ours passes `this` through); as `void __stdcall UIH_506FC0(int id, bool force)` (decorated `?UIH_506FC0@@YGXH_N@Z`) it matches. Plain `ret` handlers are cdecl. UIH_443E3E / UIH_4DF425 (parked, 2 attempts used) are most likely the same shape; so are 0x443DD0 / 0x4C7794 (they also need the unknown object at 0x639190).
130. **Out-of-line one-line setter pasted by BBT (ZTMapView::setUnk364, 0x4E0E8F)**: callers contain `sub esp,4; mov eax,[esp+4]; mov [ecx+0x364],eax; add esp,8` (the arguments are pushed, copied and popped). An inline setter gives `mov [eax+0x364],imm` and never matches; the setter must be a non-inline member defined in another file (same trick as notes 95 / 123). Seven handlers that call it (UIH_4DA138 ...) match once it is out of line.
131. **`UIControl::flagBit(n)` (inline, uicontrol.h)** compiles to `mov ecx,[eax+0x7c]; shr ecx,n; test cl,1`. A mask test `(m_flags & 2)` compiles to `test byte ptr [eax+0x7c],2` instead, so the shape of the test in the original (`shr`) tells which spelling to use. `if (c && !c->flagBit(3)) ...` is the usual handler body.
132. **ZTMapView screen (UIH_4017E5 0x4017E5)**: `find(0x1B58)` cached in g_638068, a ZTMapView (size 0x5EC; its constructor 0x51F80C initialises +0x438 / +0x43C). About 60 tiny handlers are `view = UIH_4017E5(); if (view) view->fNNNN(...)` (or the same behind a `find(id)` null check). Typed return (`ZTMapView*`) changes the decorated name of UIH_4017E5 in zoo.map. UIControl +0x38 / +0x3C are ints (a second position pair next to +0x30 / +0x34; UIH_4EF967 copies one pair into +0x40 / +0x44 and sets +0x48).
133. **Wrapper handlers whose callees are all written (session 5, rounds 612-614, 13 matches in 3 rounds)**: `Tools\calleescan.py` finds unwritten functions whose callees are all in zoo.map; they are thin wrappers and match first time as plain code: `g_flag = true; UIH_xxx(0);` (the "force the next timer tick" family: 0x5B0F93, 0x41739A, 0x427996, 0x431712, 0x4741DE; the flag is the one the tick handler tests as `g_x || !t || t >= limit`), `a(x); b(x); c(); d(x);` (cdecl, `add esp,N` after the last call), and `control = UIH_4F188A(); if (control) control->vslot21();`. Define them in a spot after their callees; they stay out-of-line (BBT pastes the 5-16 byte ones into callers, which compare.py models). Write the map line for each new function in the same round, or the next verdict counts its callers' references as unknown.
