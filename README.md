# Zoo Tycoon — matching decompilation

A work-in-progress **matching decompilation** of *Zoo Tycoon* (2001, Blue Fang Games / Microsoft),
Complete Collection `zoo.exe`.

Hello everyone. I'm rather new to all of this so please bear with me. This is the second decompilation project I've started, with Claude serving as a valuable assistant.

The goal is readable C++ source that, compiled with the original compiler (Visual C++ 6.0 SP3),
produces **the same machine code as the original game, function by function**. A function only counts when it
compiles to identical instructions *and* every call, global and string it references points to the same target
as in the original.

> **This repository contains no game code, assets or binaries.** You need your own legal copy of Zoo Tycoon.
> Not affiliated with or endorsed by Microsoft or Blue Fang Games.

## Status

Progress is measured by an independent verification tool, never by hand
(see [`Notes/VERIFIED_PROGRESS.md`](Notes/VERIFIED_PROGRESS.md)). As of 2026-10-28:

| | Functions | Share of 10,672 |
|---|---:|---:|
| Readable reconstruction (matched, real names) | 86 | 0.8% |
| Matched, honest placeholder names (to be documented) | 3 | <0.1% |
| Compiler-generated copies (verified) | 1,167 | 10.9% |
| Microsoft C runtime / import thunks (not our source) | 265 | 2.5% |

Only the first row is counted as reconstruction. It's early days.

## Target

| | |
|---|---|
| File | `zoo.exe` v12.4.0.9, 2,449,432 bytes |
| SHA-1 | `6fb3c5332b0fce758cc002ef21a9150b30471d86` |
| Compiler | Visual C++ 6.0 SP3 (Rich header build 8447), STLport 4.0 |
| Post-link | Block-reordered after linking (cold blocks moved to the end of `.text`) |

`zoo.exe` is the only code file. The language/resource DLLs contain only resources; `ijl15.dll` is Intel's JPEG library.

Because of the post-link reordering, a byte-identical `zoo.exe` can't be re-linked with public tools.
"Matching" here means every function matches; `Tools/compare.py` follows control flow and models the
reordering (inlined tiny calls, merged tail jumps, shared epilogues).

## Building and verifying

You need:
- Your own `zoo.exe` (check the SHA-1 above), placed in `Original/`
- Visual C++ 6.0 with the SP3 compiler binaries (`cl.exe`, `c1.dll`, `c1xx.dll`, `c2.dll`); a Windows XP VM works well
- STLport 4.0 headers
- Python 3 with `capstone` (`pip install capstone`) on the machine that compares

Steps:
1. Source goes in `Src/<folder>/*.cpp`, shared headers in `Src/include/`.
2. Build: run `Tools/watch.bat` in the VM, or `Tools/build_core.bat` directly. Objects land in `Results/`.
3. Verify: `python Tools/verdict.py Original/zoo.exe "Results/*.obj" --map Notes/zoo.map`
   — prints `MATCH` / `DIFF` per function, with a hint at why a function differs.

## Repository layout

| Path | Contents |
|---|---|
| `Src/` | The reconstructed source |
| `Tools/` | Build scripts, comparison and analysis tools (`compare.py`, `verdict.py`, `symcheck.py`, `classmap.py`, `show.py`, ...) |
| `Notes/zoo.map` | Function names and addresses |
| `Notes/MATCHING_NOTES.md` | Compiler habits learned so far |
| `Notes/COMPILER_LIMITED.md` | Functions our compiler build cannot reproduce |
| `Notes/READABILITY_STANDARD.md` | What counts as acceptable source |
| `Notes/classes.csv` | Classes recovered from vtables |

## Standards

- **Readable source only.** No generated code, no macro-stamped functions, no invented one-off types, no
  inline assembly. Unknown members and functions get honest placeholder names (`m_unk35C`, `UIH_4D5A49`)
  until their purpose is known. The standard is calibrated against established projects such as
  [zeldaret/oot](https://github.com/zeldaret/oot), [zeldaret/tp](https://github.com/zeldaret/tp) and
  [n64decomp/sm64](https://github.com/n64decomp/sm64).
- **No fakematches.** A function that only matches through a trick (`volatile`, dummy locals, empty blocks)
  is not counted.
- **Right targets, not just right bytes.** Every relocation is checked against the original.

## How AI is used

Much of the reconstruction is done with an AI assistant (Claude), working through the same build-and-verify
loop as a human would. Because of that, nothing is taken on trust:
- every function is compiled and compared against the original, including its call/data targets;
- progress figures come only from an independent verification tool the AI cannot modify;
- generated or placeholder code is reported separately and never counted as reconstruction.

## Related projects

These take different approaches and complement this one:
- [sharkwouter/zt1-engine](https://github.com/sharkwouter/zt1-engine) and
  [StevenGann/zt1-engine](https://github.com/StevenGann/zt1-engine) — open-source engine reimplementations
- [openzt1/openzt](https://github.com/openzt1/openzt) — enhancement/modding DLL
- [ZtModArchive](https://github.com/ZtModArchive) — the Zoo Tycoon modding archive

## Legal

This project contains only original source written to reproduce the game's behaviour, plus tools and notes.
It contains no copyrighted game files, and none are distributed. Zoo Tycoon is a trademark of Microsoft.
This project is non-commercial.

## License

CC0 1.0 Universal. You have the freedom to do anything you want with this source code. Speaking personally though, I'd like it if you'd credit me when using my source code on a project. Not a requirement, just asking.
