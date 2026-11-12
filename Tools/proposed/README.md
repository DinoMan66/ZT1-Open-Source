# Tool proposals

Changes to **protected** tools (CLAUDE.md rule 3) are made here, never in `Tools\` directly.
Free tools are edited directly - don't put them here.

One folder per change:

```
Tools\proposed\<short-name>\
    PROPOSAL.md        first line: one-line title
    compare.py         the full new version, laid out as under Tools\ (a new file becomes a protected tool)
```

PROPOSAL.md:

```
# <one-line title>

What:     the change, in a few sentences
Why:      the problem it solves, with function names / addresses
Expected: stricter | looser | neutral - and which functions should change verdict
Tested:   old vs new tool on the current build (Claude's side): the differences
```

Then the user runs, on the PC:

```
py C:\AntiCheat\anticheat.py <project> trial  <short-name>    shows the diff, re-verifies everything with both versions,
                                                              writes TRIAL.md here (what changed verdict)
py C:\AntiCheat\anticheat.py <project> accept <short-name>    installs it, backs up the old files, re-baselines,
                                                              logs it in Tools\CHANGES.md, archives the folder in accepted\
```

A looser change (functions that newly count as matched) needs evidence that it models what the real compiler or
linker does, and an explanation for every newly accepted function.
