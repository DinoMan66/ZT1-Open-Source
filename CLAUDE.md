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
3. **Protected tools change only through a proposal** (hash-locked - any direct edit fails the anti-cheat):
   Tools\compare.py, symcheck.py, verdict.py, triage_lib.py, instances.py, libmatch.py,
   build_core.bat, watch.bat, Tools\lib\*, Original\*,
   plus every project module they import and any tool added by an accepted proposal.
   To improve one, put the new version in `Tools\proposed\<name>\` with a PROPOSAL.md and ask the user to
   run `anticheat.py <project> trial <name>` (then `accept <name>`) - see "Improving the setup". All other
   tools are free to improve. Never edit files in Results\. Queue commands (Tools\queue\cmd_*.bat) run only while
   the user has enabled them in the VM for a probe session; use them for diagnostics only, never to change or
   replace a compiler, and never to write objects that get scored. The anti-cheat marks such builds as untrusted.
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
   names as soon as the purpose is known (renaming members/locals/non-exported names normally keeps every match, but rebuild and re-verify the whole file
   after a rename - on VC6 a spelling can change later functions; recorded names - JPOG exports, strings - are kept
   verbatim). Since 2026-11-10 also NOT allowed: raw offset arithmetic (`*(int*)((char*)this + 0x30)` - declare
   `m_unk30`), steering pragmas / `__forceinline`, redundant constructs added to move the compiler. A macro the
   original evidently had needs an `// original macro: <evidence>` comment. Named functions carry a `// name:`
   source tag (string / vtable / caller / guess). Details: READABILITY_STANDARD.md. Label a deliberate fakematch
   `// FIXME: fakematch`. If a function can only be matched with not-allowed code, do not commit it: add a note
   to `Notes\removed\` and move on. Do not re-add files listed in `Notes\READABILITY_REVIEW.md`; the old
   versions of deleted files are kept (reference only) in `Notes\removed\*.md`.

## Files to know (read only what the task needs)
| File | What |
|---|---|
| `README.md` | Target, compiler, build workflow, why compare.py walks control flow |
| `Tools\TOOLS.md` / `Tools\CHANGES.md` | Every tool: free or protected, what it does, how to run it / log of tool changes |
| `Notes\NOTES_INDEX.md` + `Tools\notes_index.py` | **Read this, not MATCHING_NOTES.md**: a short index of every note; print single entries with `--show <id>`, search with `--find words` |
| `Notes\MATCHING_NOTES.md` | Compiler habits + codebase facts (numbered). Too long to load whole - go through the index |
| `Notes\VC6_COMPILER.md` | Mismatch sessions: what decides VC6's registers and operand order, the tools, the stop rules |
| `Notes\OPEN_WALLS.md` | Functions parked at a register / schedule difference, with the best lead |
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
0. **Start from a list, not by exploring.** If `Tools\localai\out\PREREAD.md` exists (the user's local model
   pre-read the next targets), stage and read it first: targets in order, each with a short digest. Otherwise
   `python3 -I Tools/next.py` (`--folder gx`, `--max-size N`) ranks the unwritten functions cheapest first:
   size, naming evidence, how much of the class already matches, named callees, the closest matched neighbour.
   It is an estimate; the generated lists below stay the first stop for trivial bodies and clusters.
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
   (genshapes.py --check is an analysis aid only since 2026-10-30, not a verdict - it is a free tool now.)
   - `MATCH` done. `DIFF` open, with 2 instructions of context and a category hint.
   - `FILED` / `LIMIT` = compiler-limited. **Stop working on it.** (Exception: the one re-check described under "When a function won't match".)
   - `HUMAN` = source-type difference that survived 4 attempts: ask the user.
   Categories: encoding, regalloc, sched, shrink-wrap, inline, fp (compiler-limited after 2 attempts);
   stack (reorder local declarations), branch (swap if/else bodies), outlined (missing `inline`?), source.
5. Commit back `Notes\attempts.csv` **after every scored round** (verdict.py writes it on your side; the wall budget
   and Notes\SESSIONS.csv read it on the PC), plus `Notes\COMPILER_LIMITED.md`, `Notes\PROGRESS.md`, `Notes\zoo.map`.
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
- Don't read whole Results/*.txt dumps, decompiled\zoo.exe.c or MATCHING_NOTES.md; grep by address, and go
  through `Notes\NOTES_INDEX.md` for notes. Add new notes as short numbered entries (a finding and its
  evidence, not a diary of rounds).
- compare.py/verdict.py need `capstone` (pip) or GNU objdump.

## Mismatch sessions (walls)
A session devoted to functions that are written but do not match. Rules, in this order:
1. Classify the wall first (section above). Most "compiler" differences are source or build inputs.
2. **Budget: 6 build rounds per function per session** for a register / schedule wall, 2 real attempts for
   everything else (verdict.py counts). When it is used up, write the state in `Notes\OPEN_WALLS.md` (what differs, what
   was tried, the best lead) and take the next function. Only the user can extend a budget, per function.
   One function must never consume a session: breadth first, the cheap wins of many functions before the last
   instruction of one.
3. Never commit a steering construct (rule 7). A probe may use one to learn something; `Src\` keeps the plain form.
4. Tools, cheapest first: `Notes\VC6_COMPILER.md` (what is already known - read it before anything else);
   `Tools\similar.py` / `Tools\dis.py`; the decompiled VC6 compiler and other VC6 projects' notes, cloned in the
   session workspace (list in `Tools\vc6probe\README.md`); then `Tools\vc6probe\` - the compiler under the cdb
   debugger in the VM, logging the allocator's decisions.
5. A probe session needs the user: they create `C:\anticheat_allow_cmd.txt` inside the VM, and delete it and run
   the anti-cheat with `--rebuild` afterwards. Ask before starting one; say which probe and why. While that file
   exists every anti-cheat run is marked a probe session and publishes nothing.

## Background permuter (no usage)
`Tools\permuter\permute.py <file> <Class::method>` runs on the user's PC: it rewrites one function mechanically
(statement and declaration order, operand order, comparison and increment spellings), builds the copies in a
scratch folder `Src\zzperm\` in the VM and scores them. Use it for functions one or two instructions away at the
register / order level INSTEAD of spending rounds on them:
- **Choose its targets yourself:** whenever you park a near miss, add a line `<folder\file.cpp> <Class::method>`
  to `Notes\PERMUTER_TARGETS.txt` (commit it). `--auto` runs those first, then fills up from the last build.
- **Overnight:** ask the user to run `py Tools\permuter\permute.py --auto 10 --host` (or without --host): it
  works through the 10 closest near misses one by one, drops any that turn out not to be near misses, and writes
  a summary `Notes\permuter\AUTO_<date>.md`. Read the summary first; open a function's report only for EXACT.
- Ask the user to run it (it takes minutes to hours, unattended). Pick the target with `--list`: it ranks the
  last build's functions by bytes that differ. Only near misses (a few bytes, same size) are worth a run; a
  function tens of bytes off needs a source change by hand, not permutations (it warns at the start).
- Its report is `Notes\permuter\<file>__<function>.md`. An EXACT result is a candidate: apply the diff to the real
  file yourself, build and verify normally, and check the change reads like something a programmer would write.
- While `Tools\queue\permuter.lock` exists do not queue builds, and never touch `Src\zzperm\`.
- With `--host` it builds on the PC through `Tools\hostbuild` (seconds per round, `Results\` untouched).

## Helpers for writing and changing code
- **Before writing a function:** `python3 -I Tools/neighbours.py <va or name>` lists already-matched functions whose original code
  is most like it, with their source (`--show 2` for more). Copy how they are written (idioms, types, order), not
  their names - a neighbour is a model to follow, not evidence for a name.
- **Rounds with many small functions:** `python3 -I Tools/batch.py <folder/file.cpp> ... --results "<staged results>"`
  gives one line per function instead of reading verdict output function by function. It is a quick look: the
  verdict that counts is still verdict.py plus the anti-cheat.
- **Before writing or extending a class header:** `python3 -I Tools/fields.py <Class or vtable address>` lists every
  offset the class's methods touch through `this` (size, reads, writes, a type guess, which methods) and drafts
  the `m_unkXX` member list. It is evidence to check against the code, not a layout to paste.
- **After changing a shared header:** `python3 -I Tools/regress.py --who <header.h>` names the folders to rebuild;
  after that build, `python3 -I Tools/regress.py "<staged results>"` lists functions that matched at the last
  anti-cheat run and no longer do. A header change stays only when it reports no regressions.
- **Host builds** (`Tools\hostbuild`, when the user has set it up): a Claude session may ask for one with
  `Tools\queue\hostreq_<id>.txt` (`<id> <unix time> <folder>`) and read `Results_host\`. They are for quick
  iteration only: nothing counts until a normal VM build and the anti-cheat verify it, and progress is never
  reported from `Results_host\`.

## Local model (reads for you) - use it every session
When `Tools\localai\watch_ai.py` runs on the user's PC (`start_local_ai.bat`), a local model reads project files
on the PC and writes short answers, so the text never enters your context. Reading is your largest cost; hand
the model every job below instead of reading the input yourself:
- **Naming evidence (documentation rounds):** commit `Tools\queue\preread_<id>.txt` containing
  `--evidence 0x61f8c0 0x4d3de0` (any number of functions). For each it collects every caller's use, the strings
  and callees, and at most two name candidates with the lines behind them -> `Tools\localai\out\ev_<id>.md`.
- **Digests of the batch you chose:** `Tools\queue\preread_<id>.txt` with `--va 0x4e9989 ...` (or
  `--folder <x> --top 20`) -> `Tools\localai\out\pre_<id>.md`. PREREAD.md only covers next.py's own list.
- **Questions about any large file:** `Tools\queue\ask_<id>.json` (`{"id", "question", "files":
  ["decompiled/zoo.exe.c:100-400", "Notes/OPEN_WALLS.md"], "grep": "regex", "around": 12, "max_words": 250}`), e.g.
  "which functions call FUN_x and with which arguments" over the whole Ghidra file (with `grep`), the long notes
  in `Notes\removed\*.md`, build logs, MATCHING_NOTES entries beyond what NOTES_INDEX.md says.
- **Never wait for it.** Queue all requests for the next batch at the start of a build round, then build; read
  the answers (stage `Tools\localai\out\`) when the round is scored. A digest arrives in about a minute.
- Answers are hints from a small model: never evidence for a name, a rule or a match, never pasted into `Src\`
  or the notes. Open the lines they cite (file and line numbers) and use what those lines show.
- If nothing appears within a few minutes the watcher is not running: carry on without it.

## Documentation rounds (placeholders -> readable)
Matches with honest placeholder names (`vslotNN`, `f<va>`, `m_unkXX`) count as "decompiled, not documented", not
as readable. Each session, before writing new functions, spend one round promoting them: queue `--evidence` for
the placeholders in VERIFIED_PROGRESS.md's per-file list, rename those whose evidence holds (name tag as in rule
7, `// name: caller|string|vtable (confidence)`), rebuild the file and re-verify it. A rename never changes the
code, so it is the cheapest readable gain there is; leave a placeholder alone when the evidence is thin.

## Unverified references (map entries)
When VERIFIED_PROGRESS.md reports matched functions with unverified references, run
`python3 -I Tools/mapsuggest.py` (staged Results with `--results`): it re-compares those functions and lists the
original's target for each reference whose address is unknown (`Notes\map_suggestions.md`). Only CONFIRMED
entries (two or more matched functions, all pointing to the same address) go into the maps (`--write` adds them);
a single reference is not evidence. This raises how much the anti-cheat checks, not the match count.

## End of every session
0. Check before you stop: `Notes\attempts.csv` committed after the last scored round; `Notes\PERMUTER_TARGETS.txt`
   lists this session's near misses; the placeholders you could not name are still placeholders, not guesses.
1. Update "Current state" below (numbers from verdict/scoreall only, last build round, next step) and the notes.
2. Re-run `python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md` if notes were added, and commit `Notes\NOTES_INDEX.md`.
3. Update `README.md` in the project folder when something a visitor should know has changed: what is covered,
   new tools, how to build, the layout. Do NOT touch the block between `<!-- status:start -->` and
   `<!-- status:end -->` - the anti-cheat rewrites it with verified numbers.
4. Tell the user to run the anti-cheat. It also adds a row to `Notes\SESSIONS.csv` (readable change, verdicts,
   permuter/local-model/host-build use since the last run): read it when judging which helpers pay off; never edit it.
   On a CLEAN run it refreshes the README status and rebuilds the
   `public repository` folder (the files meant for GitHub; nothing copyrighted or personal is copied). Never write
   into `public repository` yourself, and never put game files, third-party files or anything about the user's PC
   into `Src\`, `Tools\` or `Notes\` - those folders are published.

## Improving the setup (the tools are meant to grow)
When the same manual step comes up a third time, a check misses a kind of problem, or a tool's output wastes
reading, improve the tool or write a new one. That is real progress, not a detour. Two kinds of tools:

| | Free tools | Protected tools (rule 3) |
|---|---|---|
| What | everything that helps: analysis, search, ranking, drafting, reports (show, classmap, trivial, ...) and every new helper | what decides whether a function counts: comparison, relocation check, verdicts, build scripts |
| How to change | edit or create directly, in any session | proposal in `Tools\proposed\<name>\`, the user runs trial + accept |

**Free tools** - keep them honest and findable:
- A docstring at the top: purpose, usage, inputs, outputs. One line in `Tools\TOOLS.md`; each change one line in
  `Tools\CHANGES.md` (date, tool, what and why).
- Output goes to the screen or `Notes\` - never into `Src\` (rule 7), `Results\`, `VERIFIED_PROGRESS.md` or
  `verified_functions.csv`. A free tool may suggest (rank candidates, draft code you then write by hand, flag
  problems); whether a function matches is only ever decided by verdict.py / scoreall.py and the anti-cheat.
- Protected tools must not import a free module (the anti-cheat would then lock it too). Share code by copying
  it into the protected tool through a proposal, or keep it in the free tool.
- Try a changed tool on real data (the last build, a known function) before relying on it. Delete experiments you
  don't keep (list them for the user - you can't delete files on the PC).

**Protected tools** - a proposal is one folder `Tools\proposed\<short-name>\`:
- The changed or new file(s) laid out as under `Tools\` (`compare.py`, `build_core.bat`, ...). Changes to free
  tools never go here.
- `PROPOSAL.md`: first line a one-line title, then *What* changes, *Why* (the problem, with function names and
  addresses), *Expected effect* (stricter / looser / neutral, and which functions should change verdict) and
  *Tested* (score the current build with the old and the new version on your side and list the differences).
- **Stricter** (catches wrong targets, adds a check) is welcome. **Looser** is allowed only when it models
  something the real toolchain does, with evidence from the original binary (e.g. the post-link optimizer
  pasting tiny calls into callers); every newly accepted function must be explained. Never loosen a check to get
  a stuck function through - that is the wall-classification job, not the tool's.
- Build-script changes can't be tested by the trial (the build runs in the VM): say how to test them.
- One change per proposal, small enough to read. Not proposable: `Original\`, `Tools\lib\`, the queue, and the
  anti-cheat itself (it belongs to the user - suggest improvements in words).
- The user runs `trial`: it shows them the diff, re-verifies every function with both versions and writes
  `TRIAL.md` into the proposal folder (newly accepted / newly rejected functions). Read it; fix the proposal if
  the result is not what PROPOSAL.md predicted. After `accept` the proposal moves to `Tools\proposed\accepted\`
  and `Tools\CHANGES.md` records it. Update this file if the workflow changes.

Ideas you can't do now go to the "Ideas" list at the end of `Tools\TOOLS.md`.

## Current state (2026-10-23, round 237)
- **2026-11-12 (session 5, rounds 612-614, ui batch scored with verdict.py).** 329 matched in ui (+13), 7 open as before. New: 13 thin wrapper handlers in Src\ui\uiscreenhandlers.cpp (f5b14a4, f5b0f93 and the other "force the next tick" functions f41739a / f427996 / f431712 / f4741de, f484b9a, f48173e, f47ee5d, f4ef99b, UIH_48168C / 4816B2 / 4832F9). They were found with the new free tool `python3 -I Tools/calleescan.py --max 140 --blocks 8 --skip-lib` (unwritten functions whose callees are all written; MATCHING_NOTES 133); re-run it after every scored round. What it still lists needs unnamed classes (0x63512C, 0x631CCC, 0x63193C, 0x631300, the object at 0x638FF8 / 0x63CF9C / 0x639190) - identify those first. The PC zoo.map had lost UIH_44410C / UIH_4E284A / g_63cd60 (re-added). Last build round: 614.
- **2026-11-12 (session 4, rounds 574-608, scored per batch with verdict.py).** ui batch (round 608): 311 matched, 7 open (UIImage::vslot43, UIH_443E3E, UIH_4DF425 and
  the earlier parked ones, OPEN_WALLS), 0 need a human; gx batch (round 605): 32 matched, 2 open, 3 compiler-limited; snd unchanged (55). New this session: the ZTMapView screen
  (Src\include\ztmapview.h, Src\ui\ztmapview.cpp: ZTMapView = find(0x1B58) cached in g_638068, out-of-line setUnk364, f410f84, f4ef75b),
  about 120 more plain handlers in Src\ui\uiscreenhandlers.cpp (find()-null-check, ZTMapView forwarders, the 8 UIGraph handlers, `__stdcall` UIH_506FC0), UIControl::f418a49,
  uigraph.h (class moved out of uigraph.cpp), GXVidMan::createSurface, SNDSoundResource::vf3, GXImage::isValid, UIListBoxEntry icon setters. Findings: MATCHING_NOTES 129-132
  (`ret N` + reloaded ecx = `__stdcall` free function; BBT-pasted out-of-line setter; `flagBit` shape; the ZTMapView screen). Parked: OPEN_WALLS.md "session 4". Documentation round: no placeholder
  was renamed (the local model produced no evidence worth opening). Next: run the permuter (UIImage::vslot43 / hide
  were added to PERMUTER_TARGETS.txt), `py Tools\mapsuggest.py --write`, then try the `__stdcall` form on UIH_443E3E / UIH_4DF425 once their budget is extended. Last build round: 608.
- **2026-11-12 (session 4, rounds 574-578, snd batch).** Scored with verdict.py (`Results\snd.*.obj`): 64 matched, 0 open, 1 compiler-limited (DX8Sound::instantiate).
  New: DX8Sound::release (out-of-line releaseBuffer / releaseResource helpers, note 128), the three BFPos functions (play / playLooped / updatePosition, reused `volume +=` local, note 126),
  SNDSoundResource vf1 / vf3 / vf4 / vf6 and its destructor, BFResourceHandle::reset / destructor (notes 127). vf3 returns `int` (a callee `mov eax,1` shows it).
  Budget disclosure: SNDSoundResource::vf3 used both attempts (round 576 only built a stale partial file because device_commit_files lagged: commit twice and check the size with device_list_dir
  before requesting a build); it matched in round 577. Cheap named targets are drained: what next.py still lists is deleting-destructor wrappers (compiler-generated), placeholder vtable slots whose
  class is unnamed (vtable 0x632200 "ZTMapView" slots 0x619463/68/6D/72, 0x631300 class, ZTAIMgr forwarders 0x601E1C / 0x59DA9F) and big functions (UIListBoxEntry icon trio, GXPalette::create 0x4ADACF,
  GXCanvas::clear, GXLLEAnimSet::attempt 0x40B967, GXVidMan::setupFullscreen 0x4D6894, GXImage::draw 0x61F0C8, ZTScenarioMgr slot 8 0x4B2A7F needs the out-of-line STL helpers 0x4B2A48 / 0x40A5BC typed).
  The local model's evidence (ev_*.md) gave no name for any placeholder: the documentation round renamed nothing. Next: `py Tools\permuter\permute.py --auto 10 --host`, `py Tools\mapsuggest.py --write`,
  then the UIListBoxEntry icon functions or type the ZTScenarioMgr members. Last build round: 578.
- **2026-11-12 (session 3, rounds 549-573, scored per batch with verdict.py).** ui batch (round 573): 247 matched, 1 open (UIImage::vslot43, prologue push, OPEN_WALLS),
  3 compiler-limited (UIImage::hide, UIScrollingRegion::vslot40, UIEditableText ctor), 1 needs a human (UIButton ctor, test all members in the init list); zt: 15 matched;
  gx: 30; snd: 55. New this session: UIElement has six empty virtuals and UIControl owns the deleting destructor at slot 6
  (MATCHING_NOTES 118-120), destructors of UIControl / UILayout / UIButton / UIEditableText / UIScrollingRegion and their
  deleting wrappers, UILayout slots 14/15/16/18/30/34, UIImage-owned slots 18 and 29-31, UIListBox wheel handler (slot 40),
  ZTAIMgr::vf13 (atoi), BFResourceHandle::set / release / reset and SNDSoundResource::vf4 (note 123: addRef is an
  out-of-line function pasted by BBT). Parked (OPEN_WALLS): UILayout::hide, UIListBox / UIImage / UIGraph / UIScrollBar /
  ZTMiniMap / UIRadioSet destructors, the 0x631300 class (its name is unknown), the ZT manager destructors, the unmatched
  copy constructors. Next: run `py Tools\permuter\permute.py --auto 10 --host` for the dither functions, then
  `python3 -I Tools/mapsuggest.py --write`. Last build round: 573.
- **2026-11-12 (session 2, up to round 538, UI handlers and class slots).** Last build round: 538. Verdict, whole ui batch scored together (`Results\ui.*.obj`): 217 matched, 0 open;
  gx batch 30 matched, 3 compiler-limited, 2 parked. New files: Src\ui\uiscreenhandlers.cpp (140 plain handlers), Src\include\ztentity.h, ztgame.h + Src\ui\ztgame.cpp,
  gximage.h + Src\gx\gximage.cpp, uilistbox.h (class moved out of uilistbox.cpp, setSelectedIndex added); new virtual slots in UIButton, UIStatusImage, UIRadioSet, UILayout, UIGraph,
  UIEditableText, ZTMiniMap, UIScrollingRegion (clone, vslot22/23/31/37/40) and three UIManager methods. Always score the ui batch with ui.uicontrol.obj and ui.ztgame.obj included (BBT pastes setFlag /
  markClean / ZTGame::contains). Parked: OPEN_WALLS.md (GXImage, UIListBox slots, the 0x51A5EF class, 34-slot entity base, event registry). Run `py Tools\mapsuggest.py --write` after the
  anti-cheat. Permuter targets: drawDitherMirror32, drawDitherMirror24, GXLLE::draw16, drawMirror16 (`py Tools\permuter\permute.py --auto 10 --host`).
- **2026-11-11 (rounds 462-486, breadth session).** Written with real names: SNDSoundResource / SNDSoundResourceWAV
  attempt + isValid, GXLLEAnimSet::acquire, DX8SndMgr (createDirectSound, setPrimaryBufferFormat, isValid,
  load, instantiateFor), GXImageTGA and GXImageBMP (new files gx\gximagetga.cpp / gximagebmp.cpp: getters, isValid),
  DX8Sound play / playLooped / updatePosition(BFPos*). Last snd build (round 488): 49 matched (DX8SndMgr::attach added, name guessed); ZTAIMgr::isMoveSlow/Medium/Fast (new Src\zt\ztaimgr.cpp, round 487) match. Key finding
  (MATCHING_NOTES 91): a caller's `test al,al` means the callee returns bool. Parked, all one instruction off and good
  permuter targets: DX8Sound::instantiate (+0x107), DX8Sound::play / playLooped / updatePosition(BFPos*) (note 93),
  GXImageTGA::attempt / GXImageBMP::attempt (note 92), plus the dither/draw16 family (notes 89-90). Named-target
  supply is nearly drained: what next.py still lists is unnamed vtable slots (placeholders) or STLport-string
  functions (GXVidMan::setupFullscreen 0x4D6894, GXLLEAnimSet::attempt 0x40B967, GXImage::draw 0x61F0C8). Obsolete file
  Last build round: 488.
- **2026-11-11 (rounds 455-461, mismatch session).** Sibling comparison for the dither wall (MATCHING_NOTES 89-90):
  the plain 16-bit draw 0x4F47AA and its mirrored twin 0x4F493B, written with the same skip spelling, get the
  original's registers in both; the rewrite ran in the original plain twin and was skipped in the mirrored one, so
  the original spells those skip statements differently (spelling still unknown; the count-in-edx pattern is a
  coincidence). Round 461 added Src\gx\gxlle.cpp with GXLLE::draw16 / drawMirror16 (names: guess) and the
  drawDitherMirror24 map line: draw16 differs from +0x45 (prologue schedule), drawMirror16 from +0x7 (prologue)
  and has the same skip-loop wall. Good permuter targets, with drawDitherMirror32. Last build round: 461.
- **2026-11-10 (setup update, no build rounds).** Rounds 259-452 went into the two dither functions
  (drawDitherMirror32 / 24): each is one instruction away; they are PARKED (Notes\OPEN_WALLS.md, Notes\VC6_COMPILER.md)
  under the new 6-rounds-per-session wall budget. Round 453 restored the plain skip loops in gxlledither.cpp
  (the "escape form" was a steering construct): drawDitherMirror32 is still exactly one instruction away (the
  off-screen row's lea at +0x1ee), so nothing was lost. Try `Tools\permuter` on it before any more rounds. The debugger probes moved from Probe\weights to Tools\vc6probe (free
  tools); notes are read through Notes\NOTES_INDEX.md. New rules: raw offset arithmetic, steering pragmas, name
  source tags (READABILITY_STANDARD.md). Next: breadth - the UI handlers in Notes\removed\ui__uihandlers.cpp.md,
  then clusters and trivial functions per class. Last build round: 453.
- **Mismatch clean-up (2026-10-28, rounds 238-240): 89 functions match** (was 64). Fixed: 23 `__FILE__` strings
  (#line with the original C:\aqua\src path, MATCHING_NOTES 58); GXVidMan::flip via the out-of-line
  BFWindow::isMinimized 0x4D5FB5 (note 59); DX8Sound::getVolume (note 60); instances_actions.csv corrected
  (16 rows of other classes removed, 3 re-keyed, note 61). Re-checked once and final: DX8Sound play/playLooped/
  setVolume/mute, BFLogHResult (COMPILER_LIMITED.md). Still open, needing real work: UIGraph::create (STLport
  inlining, note 27), UIEditableText ctor (note 29), ZTGameMgr::create (needs the
  ZTGameMgr constructor written; its string temporaries are the open alloc-proxy family, note 41). Last build round: 243.
- **2026-11-03 (rounds 244-258): 101 functions match** (was 89). All of DX8Sound (out-of-line DX8SndMgr::getVolume
  pasted by BBT, MATCHING_NOTES 63-64), BFLogHResult (65), UIEditableText ctor, UIGraph::create, ZTGameMgr::create
  (VC6 inline budget + hidden base ctor, 66-67). Nothing in COMPILER_LIMITED.md is "final" any more: the compiler
  is ours, a difference is an input (Notes/OPEN_WALLS.md). Only GXLLE::drawDitherMirror32 is open. Last build round: 258.
- **2026-11-03 (rounds 241-243):** GXLLE::drawDitherMirror32 control flow now matches (MATCHING_NOTES 62); only register
  assignment is left, budget used (COMPILER_LIMITED.md).
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
