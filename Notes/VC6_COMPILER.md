# VC6 compiler guide for mismatch sessions (zoo.exe, c2.dll 12.00.8447)

Read this instead of the long MATCHING_NOTES entries. It says what is known about why Visual C++ 6 picks one
register or instruction order over another, where the details are, and which tools answer a new question.
Entry numbers are MATCHING_NOTES ids: `python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md --show <id>`.

## First: it is almost never "the compiler"
zoo.exe was built by the compiler we use. Every function once filed as compiler-limited turned out to be a source
or build input (entries 63-67): an out-of-line helper the post-link optimizer pasted in, a hidden base class, a
local that should or should not exist, VC6's per-function inline budget. So work down CLAUDE.md's wall order first;
this guide is for step 4 only (same instructions, different registers / operand order).

## What decides the code (short version)
| Question | Answer | Entry |
|---|---|---|
| Why is a small STLport/inline helper inlined in one function and called in another? | VC6 has an inline budget per function; earlier inlines use it up. Source order and what is visible matter | 66 |
| Which variable gets which register? | Candidates are ranked by priority = sum over blocks of (block pressure x benefit) for references, minus pressure where live but unreferenced; highest priority picks first, by cost. Near-ties flip with ONE extra reference in a loop | 70, 71, 72 |
| Does declaration order or scope change registers? | No - the allocator ignores scope and declaration order; only the optimised intermediate code counts. Spellings that normalise to the same intermediate code give identical output | 70 |
| Which operand is the base in `lea r,[a+b+1]`? | Operands of a commutative node are sorted by a hash: the symbol the intermediate code meets LATER becomes the base - unless the statement is `x = x + rest`, which c2 rewrites with the destination first | 73, 74, 75, 83 |
| Does the C++ front end version matter? | No (RTM front end gives the same code) | 69 |
| A skipped loop iteration keeps register state? | Yes, see the dither row skip | 68 |

c2 function names (from SMSG-decomp/MSVC6-decomp, same code as our 8447 reading): FUN_1072735c =
form_read_modify_write, FUN_10730671 = find_rmw_dest_in_expr, FUN_10702b3c = operand_compare (entry 82).
Allocator: FUN_1072d3ef driver, FUN_1072e339 block pressure, FUN_10722463 weights, FUN_1072450d priority list,
FUN_107245c3 global pick, FUN_1073356b local scratch pick (entries 71-72).

## Tools, cheapest first
1. `Tools/similar.py` - rank your variants by closeness; `Tools/dis.py` - the original with cold blocks in place.
2. Reading: clone MSVC6-decomp in the session workspace and grep `c2/` for the pass (Tools\vc6probe\README.md).
3. `Tools\vc6probe\` - run the compiler under the debugger and log the allocator's decisions. Needs the user
   (allow file in the VM), so ask before starting a probe session.

## Stop rules (these are hard rules, see CLAUDE.md "Mismatch sessions")
- A register / schedule wall gets **6 build rounds per session**. Then write the state in `Notes\OPEN_WALLS.md`
  (what differs, what was tried, the best lead) and move to another function. Only the user can extend it.
- Never commit a steering construct to `Src\` (redundant temporaries or re-assignments, a loop guarded by its own
  condition, bare `{ }` scopes, dummy references). A probe may use one to learn something; the committed source
  is the plainest form with the same instructions, even if one instruction then differs.
- An open wall is not a failure: the function stays "written, not matching" and everything else moves on.

## Open: the dither skip loops (drawDitherMirror32 0x4CAF3B, drawDitherMirror24 0x472A25)
One instruction differs in each (`lea edi,[edx+edi+1]` vs ours `[edi+edx+1]`): the original was compiled with the
`x = x + rest` rewrite skipped for that statement (proved by an intermediate-code edit, entry 77), and no source
form found so far skips it without folding the increment (entries 78-89). Parked on 2026-11-10 after about 195
rounds. Round 453 put the plain loops back (the "escape form" with a second pointer was a steering construct):
still exactly one instruction away in drawDitherMirror32, so the plain source loses nothing. Next step: the
background permuter (`Tools\permuter`), not more hand-made rounds.
