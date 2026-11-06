# CLAUDE: START HERE (Zoo Tycoon matching decompilation)

Read this file first in every session. It replaces re-reading old conversations. `README.md` has the
setup (VC6 SP3 compiler, BBT block reordering); this file has the cheap way of working.
Usage limits are the bottleneck, so work in a scripted way and read as little as possible.

## ANTI-CHEAT RULES (read every session; they override anything else in this file)

A function counts only when it is real, readable C++ that the real compiler turns into the original's code.
Checked by the user's independent anti-cheat (`C:\AntiCheat\anticheat.py`, outside your reach) - a
violation fails the whole check, so there is nothing to gain from any of these:

1. **Forbidden in Src\**: inline assembly (`__asm`, `_asm`, `asm`), naked functions, `_emit`, byte arrays
   executed as code, code/data placement pragmas (`code_seg`, `data_seg`, `section`, `init_seg`,
   `alloc_text`), `#pragma comment(linker ...)`, `__declspec(allocate)`, `/alternatename`, hard-coded
   addresses cast to pointers or called (`(T*)0x638148`, `((void(*)())0x401000)()`), `#include` of anything
   that is not a header, and any .obj/.lib/.asm/.bin file. (Functions the original wrote in assembly
   are listed in the ORIGINAL ASSEMBLY section below - ask the user before touching them.)
2. **Compiler flags** (`flags.txt`, `*.cpp.flags`) only from the allowed list: /D /U /I (inside the project or
   C:\stlport), /O.., /G.., /W.., ICC -Q options for code generation. Never /B1 /B2 /Fo /link -Qlocation -Qoption.
3. **Never modify the verification tools or build scripts** (protected, hash-locked):
   Tools\compare.py, symcheck.py, verdict.py, triage_lib.py, instances.py, libmatch.py, genshapes.py,
   build_core.bat, watch.bat, Tools\lib\*, Original\*. If one needs a change, write the proposal to
   `Tools\proposed\<file>` and explain it to the user; the user reviews it and re-baselines. Never edit
   files in Results\, and never use Tools\queue\cmd_*.bat to change compilers (the build refuses them).
4. **A match needs the right targets.** compare.py checks every relocation: the call must go to the same
   function, the load must read the same global, the string must be the same string (Tools\symcheck.py).
   "relocation target differs" is a MISMATCH, never something to explain away.
5. **No justifications.** Comments or notes that argue a difference is acceptable do not change the result -
   a function verifies or it does not. Do not widen tolerances, exclude functions or relabel statuses.
6. **Honest progress.** Report progress only from `Notes\VERIFIED_PROGRESS.md` (written by the anti-cheat).
   Placeholder code (Z_<va>, UIH_<va>, f<va>/m<va>/g_<va>, m_unkXX, pad[], dummy virtuals), compiler-generated
   copies and Microsoft library code are separate tiers and are never reported as reconstruction.
   Prefer giving real names (class, method, member) over generating more placeholders.
7. **Readability standard** (`Notes\READABILITY_STANDARD.md`, calibrated against sm64/oot/mm/tp, enforced by
   the anti-cheat). Hard rules: plain text, consistent formatting (one statement per line), comments on
   non-obvious logic, the game's code written plainly. NOT allowed: types invented for one function and named
   after it (`struct Z_4DA485 { void f(); }`), one-letter methods (`X::f()`), `c0`/`v12` members, generator
   output (never let Tools\gentrivial.py / genshapes.py write into Src\ - analysis output into Notes\ only),
   macros that stamp out function bodies, verification scaffolding (probes, reference units of invented
   globals/classes, files that only force template instantiations).
   ALLOWED as honest placeholders ("decompiled, not fully documented"): offset-named members with an offset
   comment (`/* 0x35C */ bool m_unk35C;`), address-named functions/globals whose purpose is unknown
   (`UIH_4D5A49`, `f48d052`, `g_638068`), unknown vtable slots in a real class (`vf3`). Replace them with real
   names as soon as the purpose is known (renaming members/locals/non-exported names never changes the code; recorded names - JPOG exports, strings - are kept verbatim). Label a deliberate fakematch
   `// FIXME: fakematch`. If a function can only be matched with not-allowed code, do not commit it: add a note
   to `Notes\removed\` and move on. Do not re-add files listed in `Notes\READABILITY_REVIEW.md`; the old
   versions of deleted files are kept (reference only) in `Notes\removed\*.md`.

## Files to know (read only what the task needs)
| File | What |
|---|---|
| `README.md` | Target, compiler, build workflow, why compare.py walks control flow |
| `Notes\MATCHING_NOTES.md` | Compiler habits + codebase facts (numbered). Read before writing code. |
| `Notes\COMPILER_LIMITED.md` | Functions our compiler cannot match. **Never retry these.** |
| `Notes\READABILITY_STANDARD.md` | **What counts as readable source** - every file in Src must meet it |
| `Notes\READABILITY_REVIEW.md` | 2026-10-27 review: files removed / pending your decision; notes in `Notes\removed\` |
| `Notes\VERIFIED_PROGRESS.md` | **The only progress numbers to report** (anti-cheat output, honest tiers) |
| `Notes\PROGRESS.md` | Honest summary + per-file history (recorded statuses) |
| `Notes\symbols.map` | Known addresses of symbols we reference but have not written (relocation check only) |
| `Notes\zoo.map` | name = VA for every function we have written |
| `Notes\inventory.csv` | All 10,672 functions (va, size, blocks, callers, vtable refs, strings) |
| `Notes\attempts.csv` | Written by verdict.py: attempts per function, category, status |
| `Notes\generated\` | From trivial.py: `trivial_zoo.cpp`, `clusters.md`, `summary.txt` |
| `decompiled\zoo.exe.c` | Ghidra output (10 MB). Grep for the address, never read whole |

## The cheap workflow (do it this way)
1. **Choose work from `Notes\generated\` first**:
   - `clusters.md`: functions with identical code apart from addresses. Biggest: 902 x 182-byte static
     initialisers (the manager-name STLport strings, MATCHING_NOTES "STLport") - one source shape covers all.
   - `trivial_zoo.cpp`: 241 tiny functions with ready-made bodies (names unknown: FUN_<va>). Give them names
     from vtables / callers when you place them, add them to zoo.map.
2. **Batch**: a whole .cpp file per build round, not one function per round.
3. **Build round** (the user's XP VM runs `Tools\watch.bat`):
   - commit changed `Src\<folder>\*.cpp` / `Src\include\*.h` and new `Notes\zoo.map` lines;
   - commit a uniquely named `Tools\queue\request_<round>.txt` containing `round-NNN <unix time> <folder>`;
   - check `Results\DONE.txt` with device_list_dir until its mtime is newer than the request (the shared folder
     needs ~5 s), then stage only `Results\<folder>.*.obj`.
4. **Score with one command** and read nothing else:
   `python3 -I Tools/verdict.py Original/zoo.exe "<staged Results>/*.obj" --map Notes/zoo.map`
   UI handlers: `python3 -I Tools/genshapes.py --check Results/ui.uihandlers.obj --with Results/ui.uicontrol.obj --with Tools/lib/ftol.obj`
   - `MATCH` done. `DIFF` open, with 2 instructions of context and a category hint.
   - `FILED` / `LIMIT` = compiler-limited. **Stop working on it.** (Exception: the one re-check described under "When a function won't match".)
   - `HUMAN` = source-type difference that survived 4 attempts: ask the user.
   Categories: encoding, regalloc, sched, shrink-wrap, inline, fp (compiler-limited after 2 attempts);
   stack (reorder local declarations), branch (swap if/else bodies), outlined (missing `inline`?), source.
5. Commit back `Notes\attempts.csv`, `Notes\COMPILER_LIMITED.md`, `Notes\PROGRESS.md`, `Notes\zoo.map`.
6. New habits -> one numbered line in `MATCHING_NOTES.md`. End of session: update "Current state" below.
   Re-run `python3 -I Tools/trivial.py zoo` after adding many zoo.map entries.

## ORIGINAL ASSEMBLY (zoo.exe itself contains hand-written code here)
- 0x4AD794: MMX pixel routine (31 MMX instructions, emms) - not written yet.
- 0x61315B: two `int 3` breakpoints inside an `if` (likely an assert macro with `__asm int 3`).
- ~0x533BE4 / 0x533CC0 and 0x536916: `rdtsc` timing code.
These are the only places where `__asm` could be legitimate. Ask the user first; the anti-cheat will still
flag them, and the user decides whether to allow-list them.

## Code-rules profile (where names come from, what may change bytes)
- Compiler: VC6 SP3 (+ BBT post-link reordering). No RTTI, no exports: names are NOT recorded in zoo.exe except
  in strings. Evidence for names, in order: `Class::method` strings (62, mostly BFLog/assert-style messages),
  registrar class-name strings (`s_className`, Notes\instances_registrars.csv), the `C:\aqua\src\<dir>\<file>.cpp`
  paths (unit names and folders: UI, GX, SND, ...), Notes\classes.csv (Tools\classmap.py votes), MATCHING_NOTES.
- Style (follow the existing files): classes CamelCase with module prefix (`UI`, `GX`, `SND`, `ZT`, `BF`), members
  `m_camelCase`, globals `g_name`, statics `s_name`, one class per header in Src\include.
- Placeholders allowed: `m_unkXX` (offset), `UIH_<va>` / `f<va>` / `g_<va>` (address), `vfN` slots.
- Names/layout that DO reach the bytes: string literals, `__FILE__` (use `#line N "C:\\aqua\\src\\..."`),
  `__LINE__` - files with `#line N` markers (gx, snd, BFLog) must keep them when reformatting.

## When a function won't match: classify the wall first (in this order)
A pinned compiler is deterministic, so a remaining difference means an input differs. Do not call a wall class N
while class N-1 still diverges (adapted from lemiur's wall-identifier):
1. **Referent** - instructions identical, but a call/global/string target differs (symcheck note in verdict.py).
   Fix the identity/label. Never "fix" this with codegen tricks.
2. **Call set** - the set of out-of-line callees differs (verdict categories `inline` / `outlined`). Usually the
   caller's body is incomplete, an inline boundary is wrong, or a helper is open-coded. Finish the caller first.
3. **Control flow** - block/branch/return counts differ (`branch`). A source construct: separate returns vs one
   exit, `while` vs `do`, `||`/`&&` collapse, switch shape.
4. **Register / schedule** (`regalloc`, `sched`, `stack`) - only after 1-3 agree. Check in turn: variable widths
   (`unsigned char` vs `bool`/`int`), one local per meaning, declaration and first-use order, the scope/lifetime
   of temporaries, inline-helper boundaries. Only then is it compiler-limited.
**Helper recovery:** when code reaches into another class's internals, repeats a field path or has a scoped
`{ }` block, the original probably called a small accessor/inline/macro. Restore it in the owning class's header
only with evidence (the same pattern at several sites, an existing helper, a string), apply it at every site, and
rebuild: exact functions must stay exact. This is real source even when no score moves.
**Compiler-limited list:** entries filed before 2026-10-28 only because of regalloc/sched get ONE re-check against
step 4 and helper recovery (one attempt each, note the result in COMPILER_LIMITED.md); after that they are final.
**Fakematches:** if a match needs `volatile`, a dummy local, an empty block, `do{}while(0)`, `+ 0` etc., it is not a
match (MATCH-PENDING in the anti-cheat report). Use the trick as a clue to the real source, then remove it.

## Rules that save usage
- Re-read the ANTI-CHEAT RULES and this section at the start of every build round - rules fade as the
  context fills (momo5502). Keep context small: one file/class per round, fresh session for a new area.
- Routine rounds (trivial bodies, clusters, renames, helper application) run fine on a cheaper model; the
  harness (verdict.py + anti-cheat) is what keeps them honest. Save the strongest model for walls and reviews.
- Retry budget is 2 real attempts per function (verdict.py counts them), each one aimed at the wall class above. `[esp]`-encoding and ecx/eax choices
  are the compiler front end (MATCHING_NOTES "Compiler identification, revised") - don't hand-craft variants.
- Don't read whole Results/*.txt dumps or decompiled\zoo.exe.c; grep by address.
- compare.py/verdict.py need `capstone` (pip) or GNU objdump.

## Current state (2026-10-23, round 237)
- **Mismatch clean-up (2026-10-28, rounds 238-240): 89 functions match** (was 64). Fixed: 23 `__FILE__` strings
  (#line with the original C:\aqua\src path, MATCHING_NOTES 58); GXVidMan::flip via the out-of-line
  BFWindow::isMinimized 0x4D5FB5 (note 59); DX8Sound::getVolume (note 60); instances_actions.csv corrected
  (16 rows of other classes removed, 3 re-keyed, note 61). Re-checked once and final: DX8Sound play/playLooped/
  setVolume/mute, BFLogHResult (COMPILER_LIMITED.md). Still open, needing real work: UIGraph::create (STLport
  inlining, note 27), UIEditableText ctor (note 29), GXLLE::drawDitherMirror32, ZTGameMgr::create (needs the
  ZTGameMgr constructor written). Last build round: 240.
- **Readability review (2026-10-27, calibrated standard):** kept 42 files = 22 readable + 20 "decompiled, not fully
  documented" (UI classes with m_unkXX members, dx8sound vf0..vf7, ztaction, typedcall). Deleted 53 files: 16 unreadable
  (shapes_unowned, trivial_unowned, uihandlers, smallpairs*, isa, kindof, strreturn, ... = 973 functions), 26
  verification-scaffolding units (Src\stl\*, Src\reg\static_*, stl_inst*, probe) with their 26 instance lists, and 11
  scratch files. Their zoo.map lines are in Notes\removed\removed_zoo.map; each function's matching source is in
  Notes\removed\<file>.md - use those notes when re-decompiling (e.g. the 207 UIH_ handlers of uihandlers.cpp:
  rewrite them as plain functions without the UI_* macros and the one-off Z_ structs).
- **Honest numbers after the review (2026-10-27):** 97 functions written in the 42 kept files (67 in readable files, 30 in
  "decompiled, not fully documented" files); 1,184 compiler-generated copies backed by kept files (registrars, actions,
  refdata, forwarders); 251 CRT library functions + 14 import thunks (separate tiers). The anti-cheat's next run
  (Notes\VERIFIED_PROGRESS.md) gives the verified figures. The old "6,006 / 10,672 (56.3%)" is wrong - never use it.
- Three former uihandlers.cpp matches failed the relocation-target check (UIH_4D5A49 calls DeleteObject, original
  DestroyCursor; UIH_517854 g_63ea70 vs 0x63EA78; Z_58CB88::f g_63b950 vs 0x63B94E) - fix them when the handlers
  are rewritten from Notes\removed\ui__uihandlers.cpp.md.
- `__FILE__` strings: the original was built from C:\aqua\src\<dir>\<file>.cpp. Older objects carried
  "gxvidman.cpp" etc. instead; use `#line N "C:\\aqua\\src\\gx\\gxvidman.cpp"` so strings match too.
- uihandlers.cpp was deleted (readability review); its handlers and shapes are in Notes\removed\ui__uihandlers.cpp.md.
  Global-container $E shapes (MATCHING_NOTES 46) are documented in Notes\removed\reg__static_globals*.md.
- Open family: std::string default ctor - the original calls the alloc-proxy ctor 0x4012A6 out of line and keeps a
  separate allocator temporary; our VC6/STLport inlines it (MATCHING_NOTES 41; UIH_61615A and 5 copies).
- Separate tiers, never counted as reconstruction: 4,596 repeated compiler-generated / STL template / forwarder
  functions (instances_*.csv), 251 CRT library functions (Notes/libmatch.csv), 14 import thunks (Notes/importthunks.csv).
- Notes/classes.csv (Tools/classmap.py): 234 vtables with slots and vptr writers (ctors/dtors); 38 named. Tools/shapescan.py finds more copies of a compiled shape.
- compare.py now models the post-link optimizer: inlined tiny calls, merged tail jumps, `[reg+0]`->`[reg]`,
  shared epilogues (MATCHING_NOTES 5, 12, 16). Re-check old "compiler-limited" calls with that in mind.
- **STLport = 4.0, header-only**: flags `/I C:\stlport\stl40\stlport /D __STL_NO_SGI_IOSTREAMS` (Src\reg\flags.txt).
- Tools\instances.py + Notes\instances_*.csv: functions one source produces many times. Score them with
  `python3 -I Tools/instances.py Original/zoo.exe <obj> --list Notes/instances_X.csv`.
- UI work in progress: Src\ui\ (UIElement > UIControl > UIImage > concrete classes; uicontrol.h, uiimage.h,
  uiscrollable.h). Done ctors: UIControl, UIImageSet, UIScrollBar, UILayout (+ the earlier UI classes). Remaining registered-class ctors: UIMessageQueue 0x520A08, ZTMapView 0x51F80C, UIImage 0x50FE83,
  ZTGameMgr (behind create 0x527DC7), ZTWorldMgr 0x4611D4. Build all UI objects together so cross-file callees
  (UIControl::setFlag) resolve.
- UI handlers (to be rewritten plainly, see Notes\removed\ui__uihandlers.cpp.md): UIH_<va>; UIManager g_uiManager 0x638DE0, find 0x40157D; UIControl virtual
  slots show=18, hide=19, enable=26, disable=27 in uicontrol.h). ~165 more call find() (list them with the snippet in MATCHING_NOTES 35, filter 'call 0x40157d').
  Variant builds: use a scratch file named <file>VarA.cpp and delete it when done (MATCHING_NOTES 37).
- genshapes.py / gentrivial.py are ANALYSIS tools only now: their output may go to Notes\generated\ as a
  reference for writing real code by hand, never into Src\ (rule 7). Identical-code clusters:
  Notes/generated/clusters.md (trivial.py).
- After device_commit_files, check the size with device_list_dir: commits right after an edit can be stale.
- Next steps: (1) more library code: DirectX/other static libs (dxguid etc.), and check why other CRT functions
  miss (python3 -I Tools/libmatch.py Original/zoo.exe Tools/lib/LIBC_cd.LIB Tools/lib/LIBCP_cd.LIB --out Notes/libmatch.csv); (2) remaining clusters (clusters.md 8+, re-run trivial.py after excluding the
  instance lists); (3) trivial functions per class.
- Last build round: 200. Candidate list of unmatched find() callers: `python3 -I Tools/uiscan.py .` (walks inventory.csv, keeps
  callers of 0x40157D not in zoo.map / instances / shapes_failed; ~200 left, many use the
  open std::string default-ctor family).
