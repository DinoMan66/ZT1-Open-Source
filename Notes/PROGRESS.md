# Progress

## Readability review (2026-10-27, calibrated standard)

All source files were checked against Notes\READABILITY_STANDARD.md (calibrated against sm64/oot/mm/tp; details in
Notes\READABILITY_REVIEW.md). Kept: 42 files - 22 readable and 20 "decompiled, not fully documented" (real classes
whose unknown members/slots still carry honest placeholder names), with 97 functions written in them (67 + 30).
Removed: 16 unreadable files (973 functions: invented per-function types, macro-stamped functions, generator output),
26 verification-scaffolding units with their instance lists, and 11 scratch files. What the removed files matched is
kept in Notes\removed\ (one note per file, the matching source of every function). The tiers below are the state
before the review; the compiler-generated-copies tier drops to the 1,184 copies backed by kept files.

## Honest summary (rewritten 2026-10-27)

The old headline ("6,006 of 10,672 functions match, 56.3%") counted everything that compares equal:
generated placeholder code, compiler-generated copies and Microsoft's own library code. Split by what
actually exists as source:

| Tier | Functions | Share of 10,672 | Evidence today |
|---|---|---|---|
| **Readable reconstruction** (real class/function names) | **87** | **0.8%** | recorded (Notes\attempts.csv); 23 of them re-verified with relocation checks on 2026-10-27 |
| Placeholder code (Z_<va>, UIH_<va>, f<va>, pad[] structs, dummy virtuals) | ~795 | 7.4% | recorded (gentrivial/genshapes checks); 220 re-verified on 2026-10-27 |
| Compiler-generated copies (one reference function, many addresses) | 4,596 | 43.1% | recorded (Notes\instances_*.csv); **not re-verified** - reference objects not built yet |
| Microsoft CRT (LIBC/LIBCP, exact 246 + shape-only 5) | 251 | 2.4% | recorded (Notes\libmatch.csv) |
| Import thunks `jmp [__imp_X]` | 14 | 0.1% | re-verified on 2026-10-27 |

**What "readable" means:** the function and its class have real names (not address-style placeholders).
Placeholder code compiles to the same bytes, but it records the shape of the code, not its meaning, and
it does not count as reconstruction. Renaming a placeholder to its real class/function moves it up.

**Defects found by the new relocation-target check** (byte-identical, but referencing something else
than the original - these were counted as matches before):
- UIH_4D5A49 (0x4D5A49) calls `DeleteObject`; the original calls `USER32!DestroyCursor`
- UIH_517854 (0x517854) reads `g_63ea70`; the original reads 0x63EA78
- Z_58CB88::f (0x58CB88) reads `g_63b950`; the original reads 0x63B94E

**Authoritative numbers:** `Notes\VERIFIED_PROGRESS.md`, written by the anti-cheat (C:\AntiCheat\anticheat.py,
see CLAUDE.md). It re-verifies every claim from freshly built objects and never copies recorded statuses.
Run it with `--rebuild` to get the full picture; until then everything outside Src\ui is "recorded" only.

## Per-file detail (recorded statuses, kept for history)

| File | Functions | Matched | Open |
|---|---|---|---|
| Src\probe\Probe.cpp | 3 | 3 | - |
| Src\bflog\BFLog.cpp | 8 | 7 | BFLogHResult (shrink-wrap) |
| Src\gx\gxcanvas.cpp | 4 | 4 | - |
| Src\gx\gxvidman.cpp | 9 | 8 | flip (register choice) |
| Src\snd\sndsoundresource.cpp | 10 | 10 | - |
| Src\snd\sndsoundwav.cpp | 9 | 9 | - |
| Src\snd\dx8sound.cpp | 18 | 13 | getVolume, setVolume, mute, play, playLooped (register choice) |
| Src\gx\gxlledither.cpp | 1 | 0 | drawDitherMirror32 (0x4CAF3B, ~1 KB RLE blitter; attempt 1/2, frame 0x20 vs 0x24) |
| Src\reg\creates.cpp | 6 (others moved to their class files) | 5 | ZTGameMgr (ctor body laid behind create()) |
| Src\ui\uicontrol.cpp | 1 (UIControl ctor, inline UIElement root) | 1 | - |
| Src\ui\uiscrollingregion.cpp | 1 (+ctor, 2nd base UIScrollable) | 1 | - |
| Src\ui\uiradioset.cpp | 1 (+ctor, UIControl::setFlag) | 1 | - |
| Src\ui\uistatusimage.cpp | 1 (+ctor) | 1 | - |
| Src\ui\uigraph.cpp | 1 (+ctor) | 0 | map ctor inlining: original calls _Rb_tree_base ctor out of line but inlines _M_empty_initialize (MATCHING_NOTES 27) |
| Src\ui\ztminimap.cpp | 1 (+ctor) | 1 | - |
| Src\ui\uiview.cpp | 2 (ctor, create) | 2 | - |
| Src\ui\uibutton.cpp | 2 (ctor, create) | 2 | - |
| Src\ui\uilistbox.cpp | 2 (ctor, create) | 2 | - |
| Src\ui\uieditabletext.cpp | 2 (ctor, create) | 1 | ctor: original has an 8-byte frame for the colour temporary, ours 4 |
| Src\ui\uiimageset.cpp | 2 (ctor, create) | 2 | - |
| Src\ui\uiscrollbar.cpp | 2 (ctor, create) | 2 | - |
| Src\ui\uilayout.cpp | 2 (ctor, create) | 2 | - |
| Src\misc\trivial_unowned.cpp | 240 trivial bodies, placeholder classes Z_<va> (Tools/gentrivial.py) | 240 | - |
| Src\misc\ztaction.cpp + ztaction_dtor.cpp | 6 (root/middle/2 leaf ctors, root/middle dtors) | 6 | - |
| Src\misc\shapes_unowned.cpp | 394 small forwarders, placeholder names (Tools/genshapes.py) | 394 | failures in Notes\generated\shapes_failed.txt |
| Src\misc\bfrefdata.cpp | 2 (freeData, BFMemCounter::sub) | 2 | - |
| Src\ui\uihandlers.cpp | UI event handlers UIH_<va> (find control by id, show/hide/enable, list selection, hint timers, rename/colour/sound buttons) | 161 | 25 in Notes\generated\shapes_failed.txt (string default-ctor family: MATCHING_NOTES 41) |
| Src\ui\uicontrol.cpp | + setFlag body 0x4014AC | 1 | - |
| **Total written** | **~845** | **826** | 7 in COMPILER_LIMITED.md, 4 open (counts from Notes\attempts.csv) |

Repeated compiler-generated code, verified per copy with Tools/instances.py:
| Source | Copies | Matched | List |
|---|---|---|---|
| Src\include\BFRegistry.h registrars (Src\reg\reg_all.cpp) | 932 | 932 | Notes\instances_registrars.csv |
| header string constants: ctor / dtor / atexit stub / init wrapper (Src\reg\static_shapes.cpp) | 2,354 | 2,354 | Notes\instances_static_init.csv |
| `<locale>` template statics collate<char>::id + ctype<unsigned short>::id (Src\reg\static_locale.cpp) | 284 | 284 | Notes\instances_locale.csv |
| scalar deleting destructors (170) + function-local static std::string getters (25) (Src\reg\static_misc.cpp) | 195 | 195 | Notes\instances_misc.csv |
| class static `const std::string X::k("...")` ctor (20) + guarded dtor (33) (Src\reg\static_member.cpp) | 53 | 53 | Notes\instances_member.csv |
| STLport 4.0 template instantiations: vector 51, list 45, map/set 169, string 11, deque/hash_map/algorithms 25 (Src\stl\*.cpp) | 301 | 301 | Notes\instances_stl_*.csv |
| action family: leaf ctors (66), leaf dtors (74), middle ctor/dtor copies, root sdd (Src\misc\ztaction*.cpp) | 155 | 155 | Notes\instances_actions.csv (--prefix '*') |
| refcounted data per type: release (29), handle set (28), handle reset (25) (Src\misc\bfrefdata.cpp, BF_REFDATA macro) | 82 | 82 | Notes\instances_refdata.csv (--prefix '*') |
| class-static STL containers: vector init (+atexit), map header, string buffer (Src\reg\static_globals.cpp) | 53 | 53 | Notes\instances_globals.csv |
| one-line forwarders `bool X::instantiateFor(g) { return instantiate(g); }` (sound classes; same code as DX8Sound's) | 15 | 15 | Notes\instances_forwarders.csv (obj snd.dx8sound.obj, --prefix '*') |
| **Total** | **4,424** | **4,424** | |

Static libraries (no source to write; Tools/libmatch.py against the VC6 CD's LIBC.LIB / LIBCP.LIB):
| Library | Functions | List |
|---|---|---|
| LIBC.LIB + LIBCP.LIB (VC6 RTM, Tools\lib\*_cd.LIB) | 251 | Notes\libmatch.csv |
| import-library thunks `jmp [__imp_X]` (VERSION, comdlg32, IMM32, ijl15, KERNEL32) | 14 | Notes\importthunks.csv |

Old headline (all tiers together, recorded): 6,006 of 10,672 (56.3%). See the honest summary at the top.

Re-check a list: `python3 -I Tools/instances.py Original/zoo.exe Results/reg.<reference>.obj --list Notes/instances_<x>.csv`
(registrars -> reg.reg_all.obj, static_init -> reg.static_shapes.obj, locale -> reg.static_locale.obj, misc -> reg.static_misc.obj, member -> reg.static_member.obj; stl_X -> stl.stl_X.obj with --prefix '*').
Find more copies of a compiled shape: Tools/shapescan.py.

Inventory: Notes\inventory.csv lists 10,672 functions (6,486 with BBT cold blocks).

## Rounds
- 001-002: compiler setup (VC6 RTM + SP3), probe 3/3
- 003-007: BFLog, variant + flag sweeps (/O2 confirmed)
- 008-012: GXCanvas, GXVidMan
- 013-019: SNDSoundResource, SNDSoundResourceWAV, DX8Sound
- 020-024: SP4 investigation (not usable; c2.dll 8447 identified as the build stamp), flag sweep 2
- 025-028: STLport probe (4.0, header-only)
- 029-033: static initialisers (registrars, header string constants); compare.py learns BBT call inlining + tail-jump merging
- 034-035: BFLogV + BFLogDebugString; compare.py accepts BBT [reg+0] re-encoding and shared epilogues
- 036: CRT library matching (LIBC/LIBCP from the VC6 CD); compare.py inlines callees across objects
- 037-038: <locale> template-static initialisers; Tools/shapescan.py
- 039-040: scalar deleting dtors, local static strings, class static strings
- 041: STLport container instantiations (vector/list/map/set) via shapescan --all
- 042: string, deque, hash_map, sort/find instantiations
- 043-044: GXLLE::drawDitherMirror32 first draft (open); GXCanvas::lockWrite added to gxcanvas.h; Tools/similar.py
- 045-046: registered classes' create() functions; Tools/classmap.py (234 vtables, Notes/classes.csv)
- 049-056: UIRadioSet, UIStatusImage (match); UIGraph, ZTMiniMap (open); uicontrol.h, uiimage.h placeholders
- 057: UIScrollingRegion (match)
- 058: UIControl ctor (match); UIElement root class identified (vtable 0x632258, id counter 0x638D48)
- 059-064: UIView, ZTMiniMap (match: zero groups are member structs); UIGraph inlining experiments
- 065-066: UIButton, UIListBox ctors (match), UIEditableText (open); setFlag moved to uicontrol.cpp, compare/verdict register all objects for cross-file callees
- 067: UIEditableText colour variants (open); free-win clusters: 15 instantiateFor forwarders, 1 STL map function
- 068: UIImageSet, UIScrollBar (parts as 3 separate members, ext ctor 0x40E420), UILayout ctors (match, first try); their create()s moved to the class files
- 069-070: 241 trivial functions generated (Tools/gentrivial.py), all match
- 071-089: action family ctors/dtors (155 copies), class-static STL initialisers (53), import thunks (14); compare.py frameless BBT inlining; stale-commit pitfall (MATCHING_NOTES 34)
- 090-095: refcounted data handle (82 copies), Tools/genshapes.py small forwarders (340)
- 201-237: UI handlers -> 221 (UIManager::setColor345 0x40EE08, Z_4D4DCB, Z_4F16F0/Z_4FA68C caption reset, UIH_6158A0, UIH_41D565; MATCHING_NOTES 56)
- 189-200: run-time type tests (misc/isa.cpp 19, kindof.cpp 12), flagname.cpp (6), derived ??_G dtors (3, out-of-line ctor emits them); UI handlers -> 186 (UIManager::setFocus 0x44252D, switch handler 0x517854)
- 157-178: UI handlers -> 161; global containers (static_globals2-4.cpp, 61 instances); compare.py folds BBT stack cleanup (MATCHING_NOTES 45); string ctor/default-ctor experiments (41)
- 133-156: UI handlers 116 -> 151; out-of-line helpers BBT inlined (ZTGame::m443ffa, ZTPager::atFirst/atLast, UIManager::setModal, ZTGlobal148::setSound); MATCHING_NOTES 38-41
- 096-106: more genshapes families (394 total), UIControl::setFlag body found (0x4014AC), Src/ui/uihandlers.cpp UI handlers (71)
- 107-127: UI handlers to 110 (selectedId 0x443C1E found as an out-of-line BBT-inlined accessor), MATCHING_NOTES 36
