# Functions that look compiler-limited

**Re-opened 2026-11-03:** zoo.exe was built with the compiler we have (c2 12.00.8447), so a remaining difference
means an input differs (source shape, headers such as STLport, flags, or BBT), not that this compiler cannot
produce the code. The six functions that were listed as final were moved to Notes/OPEN_WALLS.md with their
history; the rows below are removed functions kept for reference.

Compiler: VC6 SP3 c1/c1xx/c2 (c2.dll 12.00.8447 = the game's build stamp), /O2.

**Revised 2026-10-21 (round 035):** several "compiler" differences were the post-link optimizer (BBT),
not the compiler: it re-encodes `[reg+0]` as `[reg]`, inlines tiny calls (`sub esp,4 ... add esp,4+n`)
and shares identical epilogues. compare.py now accepts all three (MATCHING_NOTES 5, 12, 16), which
matched GXCanvas::getDC, DX8Sound::isPlaying, DX8Sound::isLost and BFLogV.

| Function | Address | Symptom |
|---|---|---|
| (removed 2026-10-27) Src/misc/strreturn.cpp Z_5FE02D + 5 copies | 0x5FE02D.. | `lea ecx,[esi+eax]` (ours) vs `[eax+esi]` in the inlined _M_allocate_block; 4 source forms tried (round 178) |

| (removed 2026-10-27) Src/misc/smallpairs2.cpp Z_58FD9F/Z_591325 | 0x58FD9F | regalloc: original keeps `id` in ebp and reloads `arg`; ours the reverse (int and float arg tried, round 215) |
| (removed 2026-10-27) Src/misc/smallpairs2.cpp Z_479EBA/Z_47A162 | 0x479EBA | regalloc: original loads the global into ecx then `lea eax`; direct member and inline accessor tried (round 215) |
| (removed 2026-10-27) Src/misc/smallpairs2.cpp Z_43888E/Z_43C175 | 0x43888E | regalloc: original reuses esi for owner->m_1EC; return-in-if and result-variable forms tried (round 215) |
| (removed 2026-10-27) Src/misc/smallpairs.cpp Z_422B05/Z_4A0655, Z_410FFE/Z_4408B4 | 0x422B05 | regalloc: eax/ecx/edx choice for a pointer argument |
| (removed 2026-10-27) Src/ui/uihandlers.cpp UIH_4A0932 | 0x4A0932 | sched: original zeroes the row counter after the empty-list test; for/do-while/for-init forms tried (round 222) |

The ecx/eax pattern (original loads the first member into eax) is the remaining open question; the
attempts so far were judged with the old comparer, so a fresh look at one of them may be worth it later.

**Resolved 2026-10-28 (round 239):** GXVidMan::flip was not the compiler: BFWindow::isMinimized (0x4D5FB5) is a
real out-of-line function that BBT inlined into flip - mWindow sits in ecx because it was the `this` of that
call. DX8Sound::getVolume matched with an early `return 0` (the null pointer is returned as the 0).
