# Readability review - Zoo Tycoon (2026-10-27)

Every file in Src\ was checked against Notes\READABILITY_STANDARD.md (calibrated version, 2026-10-27:
honest placeholders are allowed, fabricated or generated code is not; automated rules + a manual pass).
Notes for each file that is (or may be) removed are in Notes\removed\ - one section per function with its
address, placeholder name, status and the exact source that matched, plus the full original file.

| Group | Files | Functions written in them | Compiler-generated copies they back | Decision |
|---|---|---|---|---|
| Readable - keep | 22 | 67 | 1184 | keep |
| 2 - Decompiled, not fully documented (honest placeholders: m_unkXX / UIH_<address> / slot names) | 20 | 30 | 0 | keep (documentation to-do below) |
| 4 - Verification scaffolding (probes, reference units, instantiation drivers - not the game's code) | 26 | 3 | 3406 | **delete** |
| 1 - Unreadable (invented per-function types, one-letter methods, macro-stamped functions, generator output) | 16 | 973 | 6 | **delete** |
| 3 - Scratch / obsolete files (never part of the program) | 11 | 0 | 0 | **delete** |

## Group 1 - delete (not acceptable)

| File | Functions | Copies backed | Why | Notes |
|---|---|---|---|---|
| `Src/misc/derivdtor.cpp` | 3 |  | invented per-function types: 2, e.g. Z_4E0996, Z_5017CE | removed/misc__derivdtor.cpp.md |
| `Src/misc/flagname.cpp` | 6 |  | one-letter method names: f; formatting: 5 packed + 0 overlong lines of 26; readability: macro-stamped function family FLAGNAME | removed/misc__flagname.cpp.md |
| `Src/misc/fwd11a4.cpp` | 6 |  | one-letter method names: f, g; formatting: 6 packed + 0 overlong lines of 33; readability: macro-stamped function family FWD_11A4 | removed/misc__fwd11a4.cpp.md |
| `Src/misc/gridcheck.cpp` | 4 |  | readability: macro-stamped function family GRID_CHECK | removed/misc__gridcheck.cpp.md |
| `Src/misc/isa.cpp` | 20 |  | invented per-function types: 1, e.g. Z_402232; readability: macro-stamped function family ISA | removed/misc__isa.cpp.md |
| `Src/misc/kindof.cpp` | 12 |  | invented per-function types: 1, e.g. K_40FB6A; readability: macro-stamped function family KINDOF | removed/misc__kindof.cpp.md |
| `Src/misc/lookup2.cpp` | 4 |  | one-letter method names: f; readability: macro-stamped function family TABLE_GET | removed/misc__lookup2.cpp.md |
| `Src/misc/ownerdtor.cpp` | 0 | 6 | invented per-function types: 2, e.g. Z_40D8EC, Z_635830 | removed/misc__ownerdtor.cpp.md |
| `Src/misc/shapes_unowned.cpp` | 395 |  | readability: generator output / declared placeholder file; invented per-function types: 568, e.g. Z_4020CD, Z_4020CD_B, Z_405EC4, Z_4070FE; one-letter method names: f; formatting: 485 packed + 190 overlong lines of 1608 | removed/misc__shapes_unowned.cpp.md |
| `Src/misc/smallpairs.cpp` | 46 |  | invented per-function types: 2, e.g. Z_4435B9, Z_620299; one-letter method names: f; formatting: 31 packed + 0 overlong lines of 154; readability: macro-stamped function family FWD_EMBEDDED | removed/misc__smallpairs.cpp.md |
| `Src/misc/smallpairs2.cpp` | 4 |  | invented per-function types: 2, e.g. Z_5B241E, Z_5B24AE; one-letter method names: f; formatting: 16 packed + 1 overlong lines of 96 | removed/misc__smallpairs2.cpp.md |
| `Src/misc/smallpairs3.cpp` | 2 |  | invented per-function types: 2, e.g. Z_410642, Z_410FF9; one-letter method names: f | removed/misc__smallpairs3.cpp.md |
| `Src/misc/strreturn.cpp` | 0 |  | readability: macro-stamped function family RETURN_CSTRING | removed/misc__strreturn.cpp.md |
| `Src/misc/strtemp.cpp` | 3 |  | invented per-function types: 3, e.g. Z_4BAE0A, Z_5FFF85, Z_61517E; one-letter method names: f | removed/misc__strtemp.cpp.md |
| `Src/misc/trivial_unowned.cpp` | 240 |  | readability: generator output / declared placeholder file; invented per-function types: 240, e.g. Z_40100B, Z_40100C, Z_4010E1, Z_4010E4; one-letter method names: f | removed/misc__trivial_unowned.cpp.md |
| `Src/ui/uihandlers.cpp` | 228 |  | invented per-function types: 7, e.g. Z_4B2868, Z_4D4DCB, Z_4DA485, Z_4F16F0; one-letter method names: f; readability: macro-stamped function family UI_SET_SCREEN_CONTROL; readability: macro-stamped function family UI_PAG | removed/ui__uihandlers.cpp.md |

`ui/uihandlers.cpp` is the borderline case: most of it is honest placeholder code (`UIH_<address>` handlers,
`m_unkXX` members with offsets), which the standard allows. It fails because about 55 of its functions are
stamped out by ~20 `UI_*` macros and 7 are methods `f()` of one-off `Z_<address>` structs. The alternative to
deleting it is a cleanup pass: expand the macros into plain functions (the preprocessor output is identical, so
the code is unchanged) and give the 7 methods real or address-style names, then rebuild and re-check. Its note
keeps every handler's matching source either way.

Their instance lists go with them (the reference file they are verified against is deleted):

- `Notes\instances_ownerdtor.csv`

`Notes\zoo.map` no longer lists their functions; the removed lines are in `Notes\removed\removed_zoo.map`.

## Group 2 - decompiled, not fully documented (keep)

| File | Functions | Copies backed | Why | Notes |
|---|---|---|---|---|
| `Src/bflog/BFLog.cpp` | 8 |  |  |  |
| `Src/include/bfrefdata.h` | 0 |  |  |  |
| `Src/include/dx8sound.h` | 0 |  |  |  |
| `Src/include/uicontrol.h` | 0 |  |  |  |
| `Src/include/uiimage.h` | 0 |  |  |  |
| `Src/include/uiscrollable.h` | 0 |  |  |  |
| `Src/include/ztaction.h` | 0 |  |  |  |
| `Src/misc/typedcall.cpp` | 3 |  |  |  |
| `Src/ui/uibutton.cpp` | 2 |  |  |  |
| `Src/ui/uicontrol.cpp` | 2 |  |  |  |
| `Src/ui/uieditabletext.cpp` | 2 |  |  |  |
| `Src/ui/uigraph.cpp` | 1 |  |  |  |
| `Src/ui/uilayout.cpp` | 2 |  |  |  |
| `Src/ui/uilistbox.cpp` | 2 |  |  |  |
| `Src/ui/uiradioset.cpp` | 1 |  |  |  |
| `Src/ui/uiscrollbar.cpp` | 2 |  |  |  |
| `Src/ui/uiscrollingregion.cpp` | 1 |  |  |  |
| `Src/ui/uistatusimage.cpp` | 1 |  |  |  |
| `Src/ui/uiview.cpp` | 2 |  |  |  |
| `Src/ui/ztminimap.cpp` | 1 |  |  |  |

These stay. Their unknowns are honest placeholders of the kind sm64/oot/mm/tp keep (offset-named members,
address-named functions, unknown vtable slots). Renaming members, locals and non-exported names never changes
the generated code, so documenting them later keeps every match (exported names are fixed by the binary). Give a name only when the purpose is known.

Documentation to-do per file (what would turn each placeholder into a real name):
- `bflog/BFLog.cpp`: one placeholder struct (`char pad[0x4C4]` before the HWND of the app object) - name the app class and its HWND member once the app class is known, or drop the struct and pass the HWND in.
- `include/dx8sound.h` (+ `snd/dx8sound.cpp`, 18 functions): `SNDSoundGroup` vf0..vf7 dummy slots - name the 8 virtual functions from that vtable (Notes/classes.csv), `attach`/`notify` are marked as guessed.
- `include/bfrefdata.h` (+ `misc/bfrefdata.cpp`): two members `m_unk04`, `m_unk08` of the refcounted data block.
- `include/registered_classes.h` (+ `reg/creates.cpp`, `reg/reg_all.cpp`): replace the `BF_REG_STUB`/`BF_REG_SIZED` macro stubs by plain class declarations of the 13 managers (`m_data[size]` -> real members when known).
- `include/ztaction.h` (+ `misc/ztaction*.cpp`): invented class names, `v0..v6` slots and `m_unk00`/`m_unk12C`.
- `include/uicontrol.h`, `uiimage.h`, `uiscrollable.h` and every `ui/*.cpp` class file: 2-24 `m_unkXXX` members each (UIButton alone has 10 unknown flags); needs the UI classes' members identified.

## Group 4 - verification scaffolding (delete)

| File | Functions | Copies backed | Why | Notes |
|---|---|---|---|---|
| `Src/probe/Probe.cpp` | 3 |  | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/probe__Probe.cpp.md |
| `Src/reg/static_globals.cpp` | 0 | 53 |  | removed/reg__static_globals.cpp.md |
| `Src/reg/static_globals11.cpp` | 0 | 6 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/reg__static_globals11.cpp.md |
| `Src/reg/static_globals12.cpp` | 0 | 4 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/reg__static_globals12.cpp.md |
| `Src/reg/static_globals2.cpp` | 0 | 26 |  | removed/reg__static_globals2.cpp.md |
| `Src/reg/static_globals3.cpp` | 0 | 30 |  | removed/reg__static_globals3.cpp.md |
| `Src/reg/static_globals4.cpp` | 0 |  |  | removed/reg__static_globals4.cpp.md |
| `Src/reg/static_globals5.cpp` | 0 |  |  | removed/reg__static_globals5.cpp.md |
| `Src/reg/static_globals6.cpp` | 0 | 5 |  | removed/reg__static_globals6.cpp.md |
| `Src/reg/static_globals7.cpp` | 0 | 5 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/reg__static_globals7.cpp.md |
| `Src/reg/static_globals8.cpp` | 0 | 3 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/reg__static_globals8.cpp.md |
| `Src/reg/static_globals9.cpp` | 0 | 6 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/reg__static_globals9.cpp.md |
| `Src/reg/static_locale.cpp` | 0 | 284 |  | removed/reg__static_locale.cpp.md |
| `Src/reg/static_member.cpp` | 0 | 53 |  | removed/reg__static_member.cpp.md |
| `Src/reg/static_misc.cpp` | 0 | 195 |  | removed/reg__static_misc.cpp.md |
| `Src/reg/static_shapes.cpp` | 0 | 2354 |  | removed/reg__static_shapes.cpp.md |
| `Src/reg/stl_inst10.cpp` | 0 | 5 | formatting: 13 packed + 0 overlong lines of 32 | removed/reg__stl_inst10.cpp.md |
| `Src/reg/stl_inst6.cpp` | 0 |  | formatting: 12 packed + 0 overlong lines of 26 | removed/reg__stl_inst6.cpp.md |
| `Src/reg/stl_inst7.cpp` | 0 | 50 | formatting: 64 packed + 0 overlong lines of 147 | removed/reg__stl_inst7.cpp.md |
| `Src/reg/stl_inst8.cpp` | 0 | 20 | formatting: 21 packed + 0 overlong lines of 41 | removed/reg__stl_inst8.cpp.md |
| `Src/reg/stl_inst9.cpp` | 0 | 6 | formatting: 34 packed + 0 overlong lines of 95 | removed/reg__stl_inst9.cpp.md |
| `Src/stl/stl_list.cpp` | 0 | 45 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/stl__stl_list.cpp.md |
| `Src/stl/stl_map.cpp` | 0 | 169 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/stl__stl_map.cpp.md |
| `Src/stl/stl_more.cpp` | 0 | 25 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/stl__stl_more.cpp.md |
| `Src/stl/stl_string.cpp` | 0 | 11 |  | removed/stl__stl_string.cpp.md |
| `Src/stl/stl_vector.cpp` | 0 | 51 | readability: verification scaffolding (probe / reference unit / instantiation driver), not game code | removed/stl__stl_vector.cpp.md |

These files are readable, but they are not the game's code: invented globals/classes (`g3_vecInt`,
`ProbeVirtual`, `Pod12`, explicit STL instantiations) written only so the compiler reproduces boilerplate
that zoo.exe repeats in many files. They back the 'compiler-generated copies' tier, which is dropped with them;
the real versions of this code will appear naturally inside the real source files later.

## Group 3 - scratch / obsolete (delete)

- `Src/include/regbase.h`
- `Src/misc/gridcheckVarA.cpp`
- `Src/misc/gridcheckVarB.cpp`
- `Src/misc/smallpairs2VarA.cpp`
- `Src/misc/strreturnVarA.cpp`
- `Src/reg/static_globals10.cpp`
- `Src/stltest/stltest.cpp`
- `Src/ui/uihandlersVarA.cpp`
- `Src/ui/uihandlersVarB.cpp`
- `Src/ui/uihandlersVarC.cpp`
- `Src/ui/uihandlersVarD.cpp`

## Files to delete

Groups 1, 3 and 4, plus the instance lists that are verified against them:

```
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\derivdtor.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\flagname.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\fwd11a4.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\gridcheck.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\isa.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\kindof.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\lookup2.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\ownerdtor.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\shapes_unowned.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\smallpairs.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\smallpairs2.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\smallpairs3.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\strreturn.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\strtemp.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\trivial_unowned.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\ui\uihandlers.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\include\regbase.h
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\gridcheckVarA.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\gridcheckVarB.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\smallpairs2VarA.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\misc\strreturnVarA.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals10.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stltest\stltest.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\ui\uihandlersVarA.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\ui\uihandlersVarB.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\ui\uihandlersVarC.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\ui\uihandlersVarD.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\probe\Probe.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals11.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals12.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals2.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals3.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals4.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals5.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals6.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals7.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals8.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_globals9.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_locale.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_member.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_misc.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\static_shapes.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\stl_inst10.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\stl_inst6.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\stl_inst7.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\stl_inst8.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\reg\stl_inst9.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stl\stl_list.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stl\stl_map.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stl\stl_more.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stl\stl_string.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Src\stl\stl_vector.cpp
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_ownerdtor.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals11.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals12.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals2.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals3.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals4.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals5.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals6.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals7.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals8.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_globals9.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_locale.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_member.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_misc.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_static_init.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl10.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl6.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl7.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl8.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl9.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl_list.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl_map.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl_more.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl_string.csv
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\instances_stl_vector.csv
```

Notes written by the earlier (strict) review for files that are now kept - no longer needed:

```
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\bflog__BFLog.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__bfrefdata.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__dx8sound.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__registered_classes.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__uicontrol.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__uiimage.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__uiscrollable.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\include__ztaction.h.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\misc__bfrefdata.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\misc__typedcall.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\misc__ztaction.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\misc__ztaction_dtor.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\reg__creates.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\reg__reg_all.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\removed_zoo.map
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\snd__dx8sound.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uibutton.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uicontrol.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uieditabletext.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uigraph.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uiimageset.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uilayout.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uilistbox.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uiradioset.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uiscrollbar.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uiscrollingregion.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uistatusimage.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__uiview.cpp.md
C:\OpenSourceProjects\ZooTycoonDecompiled\Notes\removed\ui__ztminimap.cpp.md
```

