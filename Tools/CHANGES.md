# Tool changes

Newest last. Protected tools change only through `anticheat.py trial/accept`; free tools are logged here by hand.

- 2026-10-30 **setup**: tools split into free and protected (Tools\TOOLS.md, CLAUDE.md "Improving the setup"); protected
  tools now change through Tools\proposed\<name>\ + anticheat.py trial/accept. genshapes.py is no longer protected
  (analysis aid since the readability review; the anti-cheat never used it).
- 2026-11-10 **notes_index.py** (free, new): index of MATCHING_NOTES.md with --show / --find, so sessions stop loading 80 KB of notes.
- 2026-11-10 **vc6probe\** (free, moved from Probe\weights): debugger probes of c2.dll, with a README; Notes\VC6_COMPILER.md is the guide.
- 2026-11-10 **localai\watch_ai.py** (free, new): local model reads long files and reports a short answer (Tools\queue\ask_*.json).
- 2026-11-10 **anti-cheat** (the user's): PC calibration of the readability checks, probe-session detection, README status block, `public repository`.
- 2026-11-11 **permuter\permute.py** (free, new): background permuter, scratch builds in Src\zzperm, report in Notes\permuter. Tested against a stand-in build machine only; the first run in the real VM is its real test.
- 2026-11-11 **fields.py** (free, new): class fields recovered from the methods' use of `this`. Checked against TViewport's known layout (JPOG) and UIControl (Zoo).
- 2026-11-11 **regress.py** (free, new): shared-header guard (`--who`, and regressions against Notes\verified_functions.csv).
- 2026-11-11 **hostbuild\hostbuild.py** (free, new) and `permute.py --host`: builds on the PC into Results_host\. Tested with a stand-in compiler only; `--check` is the real test on the PC.
- 2026-11-11 **neighbours.py** (free, new): nearest matched neighbours of a function, by its original code (masked registers/numbers, 3-gram prefilter + sequence ratio).
- 2026-11-11 **batch.py** (free, new): one table of verdicts for every function of the given source files (quick look, not the verdict).
- 2026-11-11 **permuter\permute.py**: `--list` now ranks the last build's near misses by bytes that differ (via batch.py); warns at the start when the target is not a near miss. First real run (JPOG TGFXFileInstanceObject::Render, 204 bytes off) found nothing in 2,117 variants - as expected for a big difference.
- 2026-11-11 **anti-cheat** (the user's): checker self-test [4b] - every run, up to 20 matched functions are compared with one byte of the original changed and at a wrong address; any acceptance is a FAIL.
- 2026-11-11 **localai\watch_ai.py**: works with llama.cpp's llama-server as well as Ollama (finds either, waits while the model loads, thinking off, uses the server's context); new `start_local_ai.bat` starts model + watcher.
- 2026-11-11 **next.py** (free, new): ranks unwritten functions by estimated cost, so sessions start from a list.
- 2026-11-11 **localai\preread.py** (free, new): local-model digests of next.py's top targets before a session (PREREAD.md); start_local_ai.bat runs it, watch_ai.py keeps PREREAD.md current.
- 2026-11-11 **permuter\permute.py**: `--auto N` overnight mode over the closest near misses, with a summary report.
- 2026-11-11 **mapsuggest.py** (free, new): map entries for unverified references, written only when two or more matched functions agree.
- 2026-11-11 **hostbuild\hostbuild.py**: `--check all`; JPOG reads Results\ALL.txt directly; folders without .cpp (headers only) are skipped.
- 2026-11-11 **anti-cheat** (the user's): session ledger [5b] - one row per run in Notes\SESSIONS.csv (kept out of the public repository).
- 2026-11-12 **localai\watch_ai.py**: answers cite the file in each labelled section (they had copied the example's MATCHING_NOTES.md); runs `Tools\queue\preread_<id>.txt` requests from sessions.
- 2026-11-12 **localai\preread.py**: `--va` (digests of chosen functions) and `--evidence` (naming evidence for placeholders: callers' use, strings, candidates with their lines).
- 2026-11-12 **permuter\permute.py**: `--auto` runs Notes\PERMUTER_TARGETS.txt (written by sessions) first, then moves it to Notes\permuter\.
- 2026-11-12 **next.py**: Zoo map names shown as Class::method.
- 2026-11-12 **CLAUDE.md**: local model used every session (concrete jobs, queue-then-build), documentation rounds, attempts.csv after every scored round, PERMUTER_TARGETS.txt.
- 2026-11-12 **localai\watch_ai.py**: when the model server dies mid-answer (crash, window closed) the question stays queued and the watcher waits for the server, instead of saving the error as an answer; a request that kills the server three times is set aside as out\<id>.failed.txt. preread.py re-asks questions whose saved answer was such an error.
- 2026-11-12 **calleescan.py** (new, free): lists unwritten functions whose callees are all already written / known; the same scan (as a throwaway script) found the 13 wrapper handlers matched in session 5 (rounds 612-614).
