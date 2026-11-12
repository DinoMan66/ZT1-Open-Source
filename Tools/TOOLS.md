# Tools - Zoo Tycoon

Every tool in `Tools\`, what it does and whether it is **free** (improve it directly) or **protected**
(changes only through `Tools\proposed\<name>\` + the user's `anticheat.py trial/accept`; CLAUDE.md rule 3 and
"Improving the setup"). Add a line when you add a tool; log every change in `Tools\CHANGES.md`.
Python tools run with `python3 -I Tools/<tool>.py ...` on Claude's side or `py Tools\<tool>.py ...` on the PC.

## Protected - decide what counts

| Tool | What it does |
|---|---|
| `compare.py` | Compares compiled functions with `Original\zoo.exe`, following control flow and modelling the post-link optimizer (inlined tiny calls, merged tail jumps, shared epilogues) |
| `symcheck.py` | Relocation-target check: every call, global and string must point to the same target as in the original |
| `verdict.py` | One-command build verdicts (MATCH / DIFF / FILED / LIMIT / HUMAN) with the retry budget; writes `Notes\attempts.csv` |
| `triage_lib.py` | Shared helpers for verdict.py and trivial.py (difference categories) |
| `instances.py` | Verifies functions compiled many times from one source (header statics, inline helpers) against `Notes\instances_*.csv` |
| `libmatch.py` | Finds Microsoft CRT functions in zoo.exe by comparing every member of `Tools\lib\*.LIB` |
| `build_core.bat` | The build: compiles `Src\<folder>\*.cpp` with VC6 SP3 in the VM, writes `Results\` |
| `watch.bat` | VM build watcher: waits for `Tools\queue\request_*.txt` and runs build_core.bat |
| `lib\*` | Reference Microsoft libraries (not published) |

## Free - help with the work

| Tool | What it does |
|---|---|
| `permuter\permute.py <file> <Class::method>` | Background permuter (PC + VM, no AI usage): mechanical rewrites of one function until it matches; report in `Notes\permuter\`; `--list` ranks the real near misses of the last build (bytes differ); for functions a few bytes off, not big differences; `--auto N` works through `Notes\PERMUTER_TARGETS.txt` and then the closest near misses overnight (summary `Notes\permuter\AUTO_<date>.md`) |
| `neighbours.py <va or name>` | Nearest matched neighbours: the already-matched functions whose original code is most like the target's, with their source - read before writing a function (`--show N`, `--top N`, `--all`) |
| `batch.py <folder\file.cpp> ...` | Judges every function of the given files in one table (MATCH / DIFF / size / first difference); `--open`, `--host`, `--results DIR` - for rounds of many small functions; a quick look, not the verdict |
| `next.py` | Which functions to write next: unwritten functions ranked by estimated cost (size, naming evidence, class progress, named callees, closest matched neighbour); `--folder`, `--max-size`, `--json` |
| `mapsuggest.py` | Map entries for references the anti-cheat could not check: re-compares matched functions, takes the original's targets, proposes entries (`Notes\map_suggestions.md`); `--write` adds only those confirmed by two or more functions |
| `fields.py <Class or vtable>` | Fields of a class from its methods in the original binary: every offset touched through `this`, with size, reads/writes, a type guess, and a draft `m_unkXX` member list |
| `regress.py --who <header>` / `regress.py <results>` | Shared-header guard: which folders a header reaches, and which functions matched at the last anti-cheat run but no longer do |
| `hostbuild\hostbuild.py` | Compile on the PC without the VM (`--setup`, `--check <folder>` / `--check all`, `<folder>`, `--watch`); results in `Results_host\`, never trusted - for the permuter (`--host`) and quick iteration |
| `notes_index.py <notes.md>` | Index of the notes (`Notes\NOTES_INDEX.md`); `--show <id>` prints one entry, `--find words` searches - read notes through this, not whole |
| `localai\watch_ai.py` | Runs on the PC: a local model (llama-server or Ollama; `localai\start_local_ai.bat` starts model + watcher) reads files named in `Tools\queue\ask_<id>.json` and writes a short answer to `Tools\localai\out\` - saves Claude's usage on long inputs; answers are hints, not evidence |
| `localai\preread.py` | Local-model digests: of `next.py`'s top targets (PREREAD.md, run by `start_local_ai.bat`), of chosen functions (`--va`), and naming evidence for placeholders (`--evidence`, out\ev_*.md); a session asks via `Tools\queue\preread_<id>.txt` |
| `vc6probe\` | Mismatch sessions: the VC6 compiler under the cdb debugger in the VM, logging its register allocator, intermediate code and address modes (`vc6probe\README.md`) |
| `show.py <va>` | Everything about one function: inventory row, Ghidra's C, full disassembly with cold blocks |
| `dis.py` | One function of zoo.exe with all its blocks, laid out as a compiler would have (entry first, cold blocks back in place) |
| `classmap.py` | Classes from vtables: methods, constructors/destructors, name guesses -> `Notes\classes.csv` / `classes.md` |
| `trivial.py zoo` | The no-judgment work: trivial bodies and identical-code clusters -> `Notes\generated\` |
| `gentrivial.py` | Turns trivial.py's bodies into C++ drafts - into `Notes\generated\` only, never `Src\` |
| `genshapes.py` | Draft C++ for small forwarding functions; `--check` compares them (analysis aid, not a verdict) - drafts into `Notes\` only |
| `shapescan.py` | Finds unmatched functions whose code equals one of our compiled functions (candidate copies) |
| `similar.py` | Ranks variants of one function by closeness to the original (helps choose between attempts) |
| `uiscan.py <root> [va ...]` | Unmatched functions that call a given target (default UIManager::find 0x40157D) |
| `inventory.py` | Lists every function in zoo.exe (recursive descent, BBT-aware) -> `Notes\inventory.csv` |
| `peinfo.py <exe>` | PE header summary: timestamp, linker version, image base, sections |
| `mdf2iso.py` | Converts an Alcohol 120% .mdf disc image to .iso (for mounting the game CD in VirtualBox) |
| `unzip.vbs` | Extracts a zip with the Windows shell (no extra tools on XP) |
| `export_decompiled.bat` | Ghidra headless export of `decompiled\zoo.exe.c` (run on the PC) |
| `export_more.bat` | Second Ghidra pass: creates missed functions from inventory.csv and re-exports |
| `ghidra\*.java` | Ghidra post-scripts used by the two export scripts |
| `ghidra_path.txt` | Your Ghidra folder (machine-specific - don't publish) |
| `calleescan.py` | Unwritten functions whose callees are all known (written in zoo.map, or `--symbols` for symbols.map): cheap wrapper targets. `--min/--max/--blocks`, `--skip-lib`. Re-run after every scored round (each match makes more qualify). Free tool, screen output only. |

## Ideas

Tools worth building when there is time (add yours; remove an idea when it's done or dropped):
- (none yet - add yours)
