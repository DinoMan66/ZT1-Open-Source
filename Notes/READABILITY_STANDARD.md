# Readability standard (calibrated 2026-10-27, PC update 2026-11-10)

The goal of these projects is **human-readable source code** that the original compiler turns into the
original program. A byte match is necessary, not sufficient. Every source file is in one of three tiers:

| Tier | Meaning | Kept? |
|---|---|---|
| **Readable** | Meets every rule below with real names throughout. | yes |
| **Decompiled, not fully documented** | Real code, but some unknowns still carry *honest placeholder* names (below). | yes - documentation to-do |
| **Not acceptable** | Breaks a hard rule: fabricated, generated or unreadable code. | no - delete, keep notes in `Notes\removed\` |

This is the line the big community projects draw. Measured on 2026-10-27 over their game code:

| Project | Files with offset-named members | Files with address-named functions | Invented per-function types / generated code |
|---|---|---|---|
| [zeldaret/tp](https://github.com/zeldaret/tp) | 72% (`/* 0x22F */ s8 field_0x22f;`) | 0% | none |
| [zeldaret/mm](https://github.com/zeldaret/mm) | 33% (`unk_` names) | 39% (`func_80XXXXXX`) | none (21 address-named stand-in structs in 7 files) |
| [zeldaret/oot](https://github.com/zeldaret/oot) | 26% | 30% | none (10 stand-in structs in 5 files) |
| [n64decomp/sm64](https://github.com/n64decomp/sm64) | 8% (24% use `pad`/`filler`) | 4% | none |

PC decompilations measured on 2026-11-10 (the first calibration used console games only):

| Project | What it is | Result under these rules |
|---|---|---|
| [homm3-decomp](https://github.com/sushi-shi/homm3-decomp) | Matching, VC6 SP3 like Zoo, AI agents under written rules | 670 of 721 files readable; audits remove raw offset arithmetic, steering pragmas, gotos, alias unions |
| [fnv_decomp](https://github.com/momusdigital/fnv_decomp) | Matching, all functions | The counter-example: ~7,400 raw offset reads, ~2,000 dummy locals, 213,000 `FUN_`/`DAT_` references, inline assembly |
| [tomb3](https://github.com/Trxyebeep/tomb3) / [TOMB4](https://github.com/Trxyebeep/TOMB4) / [TOMB5](https://github.com/Trxyebeep/TOMB5), [SpaceCadetPinball](https://github.com/k4zmu2a/SpaceCadetPinball), [cdcEngineDXHR](https://github.com/rrika/cdcEngineDXHR) | Working rewrites | Good names; a quarter to a third of files have no comments at all |

So honest unknowns are normal in accepted, "matching" source. What none of them contain is code invented to
make the compiler reproduce bytes: per-function fake classes, generator output, macro-stamped functions.

## Hard rules (break one -> not acceptable)

1. **Plain text.** ASCII/UTF-8 source that opens in any editor. No binary files in `Src\`.
2. **Logical structure and formatting.** Consistent indentation and whitespace; one statement per line;
   blocks, functions and loops visibly delimited; short lines (Buse & Weimer: long lines and many
   identifiers per line are the strongest negative predictors of readability).
3. **No invented names that pretend to be knowledge.** Not allowed: a type invented for one function and
   named after it (`struct Z_4DA485 { ...; void f(); }`, `K_40FB6A`), one-letter function names (`X::f()`,
   `g()`), letter+digit members without meaning (`c0`, `v12`). An honest placeholder says "unknown"; these
   pretend to be a design that never existed. Also not allowed: **raw offset arithmetic** in place of a field,
   `*(int*)((char*)this + 0x30)` - declare the field (`/* 0x30 */ int m_unk30;`) even when its purpose is unknown.
4. **Comments.** Files with real logic explain non-obvious logic, design decisions and compiler-driven
   source shapes. A deliberate fakematch is labelled as one (`// FIXME: fakematch`, as tp does). A well-named file
   with no comments at all is not deleted: it counts as "decompiled, not fully documented" until commented.
5. **Readability first - the game's code, written plainly.** Not allowed: generator output
   (gentrivial/genshapes), macros that stamp out whole functions at file or class scope (a small statement macro
   used inside functions is ordinary code), verification scaffolding (probes,
   "reference units" of invented globals/classes, files that only force template instantiations), and of
   course inline assembly / emitted bytes (anti-cheat rules 1-6).

**Macros the original evidently had.** When many classes carry the same boilerplate functions (JPOG: the
`CreateObject` / `CreateObjectInPlace` / `GetClass` set of every Toshi class; MFC message maps in other games),
the original used a macro, and one macro is the faithful reconstruction. It is allowed when a comment directly
above the `#define` starts with `original macro:` and gives the evidence (how many classes have the identical
functions, and what differs between them). The anti-cheat lists these macros in its report.

## Honest placeholders (allowed -> "decompiled, not fully documented")

- Unknown members named by offset, ideally with the offset comment: `/* 0x35C */ bool m_unk35C;`,
  `field_0x10`, documented padding `char pad[0x4C4];  // app object fields before m_hwnd`.
- Functions and globals whose purpose is not known yet, named by address: `UIH_4D5A49()`, `f48d052()`,
  `g_638068`, `FUN_`/`DAT_` (like `func_80XXXXXX` / `D_80XXXXXX` in oot/mm).
- Unknown virtual slots in a real class: `virtual void vf3();`, `_Slot12`.
- A forward declaration of an unknown callee or type by address, in moderation (oot/mm do this too).

Placeholders are replaced by real names as soon as the purpose is known. Most names never reach the machine code
(members, locals, parameters, non-exported functions), so renaming them normally keeps every match - but
**rebuild and re-verify the whole file after a rename**: on VC6 an identifier's spelling can change the code of
later functions in the same file (homm3-decomp, "names can change bytes"). Names that
ARE recorded in the binary are evidence, kept verbatim (including misspellings) and never "improved":
- JPOG: every exported function's decorated name encodes its class, name and parameter types - renaming one of
  those changes the export table;
- string literals, `__FILE__` paths and assert text (Zoo `C:\aqua\src\...`, JPOG `Z:\Toshi\Source\...`);
- in files that use `__LINE__` or `#line`, moving lines changes bytes too (layout changes are checked there).
An invented name is fine but never presented as original; when the purpose is unknown, keep the placeholder.

**Where a name comes from** (Zoo above all, whose binary records no function names). A function, class or global
that gets a real name carries a short source tag in the comment at its definition:
`// name: string` (a log/assert string names it), `// name: vtable` (slot of a named class), `// name: caller`
(its only role is clear from its callers), `// name: guess (high|medium|low)` (inferred from what the code does).
JPOG's exported names need no tag. A `guess` is a description, not the original name; raise or replace it when
better evidence turns up (convention from fnv_decomp).

**One address, several functions.** The linker merges identical functions, so one address can stand for a
method of many classes. Call it through the receiver's own class (`chunk->isLoaded()`), never by the name another
class gave the same bytes.
Once a file is documented, it is documented completely (zeldaret mm CONTRIBUTING).

Always allowed because they are conventional: loop counters `i/j/k`, coordinates and components with one digit
(`x1`, `y2`, `u0`, `v1`, `r0`), matrix elements `f11..f44` / `m00..m33`, symbols inside a written-out formula,
well-known abbreviations (`hr`, `dt`, `id`).

Cleanup debt, reported per file but not a failure: `goto` (rewrite as structured flow unless the original's shape
needs it - homm3-decomp went from 316 to 31).

## Fakematches (function level -> MATCH-PENDING)

A function whose bytes match only through a trick that steers the compiler is **MATCH-PENDING**: reported, never
counted as matched, and treated as open work (the trick points to the real source - usually a missing inline
helper, a wrong type or two variables merged into one). Checked automatically: `volatile` on a local or on
ordinary data (allowed with a `// volatile: <evidence>` comment), a local that is never used, an empty `if`/`else`
body, a bare `;` statement (empty loop bodies and `case X: ;` are fine), `do { } while (0)` outside a macro,
self-assignment, `+ 0` / `* 1`, padding or dummy virtual functions, and (2026-11-10, from homm3-decomp's rules)
the same assignment repeated right after its block, a loop guarded by an `if` with the loop's own condition,
`__forceinline`, and code compiled under `#pragma inline_depth / auto_inline / optimize / intrinsic / function`
(allowed only with an `// original: <evidence>` comment on the pragma line). Also never committed, though not
machine-checked: bare `{ }` scopes, extra temporaries, alias union members or unreachable calls added only to
move the compiler. Not fakematches: a `volatile` pointer type in a cast or call argument
(`InterlockedIncrement((volatile LONG*)&n)` is what the Windows API asks for), component indexing
(`p[3 * i + 0]` next to `+ 1`, `+ 2`). Period idioms are NOT fakematches:
`*dst++ = *src++`, `goto fail` cleanup, a long switch, the original's own bugs (label them with a comment).
(Rules adapted from lemiur's decomp-code-rules, R17 and section F.)

## How it is checked
- Automated: `C:\AntiCheat\anticheat.py` stage [2b] FAILS files that break a hard rule (machine-checkable parts),
  and reports placeholder files as "decompiled, not fully documented" (info, not a failure).
- Fakematches: stage [2b] lists them as warnings and the report counts those functions as MATCH-PENDING.
- By hand: plausibility and comment quality can't be fully automated - review new files against rules 4-5.

## Sources
- User criteria (2026-10-27): plain text, logical structure, descriptive naming, comments, readability first.
- Calibration repos: [sm64](https://github.com/n64decomp/sm64), [oot](https://github.com/zeldaret/oot), [mm](https://github.com/zeldaret/mm), [tp](https://github.com/zeldaret/tp)
- [momo5502: Letting AI agents decompile a game](https://momo5502.com/posts/2026-10-09-game-decompilation/)
- [zeldaret mm CONTRIBUTING](https://git.new.deadbsd.org/falso/mm/src/commit/48a51163894ea9836702f415345c06531ac4fff1/CONTRIBUTING.md), [REVIEWING](https://git.new.deadbsd.org/falso/mm/raw/branch/main/docs/REVIEWING.md)
- [doldecomp/melee FAQ](https://github.com/doldecomp/melee/wiki/FAQ)
- [Chris Lewis: Using coding agents to decompile N64 games](https://blog.chrislewis.au/using-coding-agents-to-decompile-nintendo-64-games/)
- [Buse & Weimer: Learning a metric for code readability](https://web.eecs.umich.edu/%7Eweimerw/p/weimer-tse2010-readability-preprint.pdf)
- [isledecomp CONTRIBUTING (MSVC-era matching project)](https://git.mattkc.com/isledecomp/isle/raw/commit/cb5d46234eaa05e359ecd67422036cf3b0ed0904/CONTRIBUTING.md)
- PC calibration (2026-11-10): [homm3-decomp](https://github.com/sushi-shi/homm3-decomp) (AGENTS.md, docs/reconstruction, docs/matching/naming.md), [fnv_decomp](https://github.com/momusdigital/fnv_decomp) (name source tags)
- [lemiur: Game-Decompilation-Skill-For-Claude (decomp-code-rules)](https://github.com/lemiur/Game-Decompilation-Skill-For-Claude)
- [Decomp Academy: enum sizing and naming](https://decomp-academy.dev/courses/gamecube-c/lesson/advanced-enum-sizing)
