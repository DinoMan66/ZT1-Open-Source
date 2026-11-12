# vc6probe - looking inside the VC6 compiler (c2.dll, build 8447)

Free tools (Tools\TOOLS.md). They run the game's compiler under the `cdb` debugger inside the VM and log what its
optimizer decides, so a register / instruction-order difference can be explained instead of guessed at.
They only read the probe inputs and write logs to `Results\`; they are never part of a build and nothing they
produce counts as a match. Moved here from `Probe\weights` on 2026-11-10 (that folder can be deleted).

**Use them only in a mismatch session, and only after the wall order in CLAUDE.md says the difference is at the
register / schedule level.** Read `Notes\VC6_COMPILER.md` first: most questions are already answered there.

## Running a probe

1. The user creates `C:\anticheat_allow_cmd.txt` **inside the VM** for the session (the build refuses queue
   commands without it) and has Debugging Tools for Windows (x86) installed (`cdb.exe`).
2. Put the source to examine in `Tools\vc6probe\in\<name>.cpp` (a copy of the unit, or a cut-down function).
3. Commit `Tools\queue\cmd_<id>.bat` with one line, e.g. `call "%ROOT%\Tools\vc6probe\autodump.bat"`, then a normal
   build request. The command runs before the compile; its console output is in `Results\cmd.txt`.
4. Stage only the log you need from `Results\` (they can be large) and read it with `qprio.py` or grep.
5. End of session: the user deletes `C:\anticheat_allow_cmd.txt` and runs the anti-cheat with `--rebuild`.
   While that file exists the anti-cheat marks every run as a probe session and does not publish its numbers.

## The probes

| Script | Log (`Results\<name>.*`) | What it shows |
|---|---|---|
| `autodump.bat` | `.weights.txt` | The global register allocator: priority list of candidates, per-block priority updates (`Q` lines), each global pick with its costs (`G`), local scratch picks (`T`, `A`, `B`), interference edges (`E`), blocks of each candidate (`P`) |
| `qprio.py <weights.txt> [ids]` | - | Sums the `Q` lines per variable: why one variable outranks another, block by block |
| `ildump2.bat` (`ildump.bat` older) | `.il.txt` | The intermediate code exactly as c2 receives it from the front end, one tuple per line |
| `blkdump.bat` | `.blocks.txt` | Basic-block order and successors at every depth-first walk |
| `amdump.bat` | `.am.txt` | Every address operand c2 builds (base / index, source line) |
| `adddump.bat` | `.add.txt` | Every call of the address-mode matcher with its operand list |
| `bothdump.bat` | `.add.txt` | `adddump` + `amdump` + every `x = x + rest` rewrite (form_read_modify_write) |
| `deldump.bat` | `.del.txt` | Tuples removed after the rewrite pass starts, and each priority computation |
| `watchdump.bat` + `watch.txt` | `.watch.txt` | Hardware write breakpoints on up to 4 addresses (c2's heap is deterministic per input) |
| `norwdump.bat` + `norw.txt` | `.norw.txt`, `.norw.obj` | **Analysis only:** forces one rewrite to be skipped by editing c2's intermediate code in memory, to see what the code would be. Its object is not a build result and must never be scored |
| `dump.bat` + `weights.cdb`, `dumplist.cdb` | `<name>.weights.txt` next to the source | Manual variant, run by hand in the VM |

The `auto*.cdb` files are the debugger scripts the batch files load; each starts with a comment saying which c2
function it hooks and what it prints. Addresses are for c2.dll 12.00.8447 at its preferred base 0x10700000.

## Reading the compiler instead of probing it

Claude's side, no VM needed (clone in the session workspace, then grep):
- `git clone --depth 1 https://github.com/SMSG-decomp/MSVC6-decomp` - a Ghidra decompilation of the VC6 compiler
  (RTM 8168) with recovered names: `c2/` is the optimizer (register allocation, inlining, instruction selection).
  Our function addresses map to its names in `Notes\VC6_COMPILER.md`.
- `git clone --depth 1 https://github.com/SMSG-decomp/MSVC6-tooling` - probes with expected output and models of
  inlining, frame ordering, the linker.
- Other VC6 matching projects document the same compiler from the source side: homm3-decomp (`docs/vc6/`),
  snail (`tools/match/c2/`), motocross-madness-2-decomp (`docs/VC6_OPERAND_ORDER.md`).
Read these for understanding only; never copy their code into `Src\`.
