# Removed: Src/probe/Probe.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (3)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x4010b6 | `ProbeCopy@` | matched (zoo.map) |
| 0x4010c7 | `ProbeGet@` | matched (zoo.map) |
| 0x4010da | `ProbeIdentity@` | matched (zoo.map) |

## Matching source per function

### 0x4010b6 `ProbeCopy@`

```cpp
// 0x4010B6: copy-construct an int in place (looks like an STL construct() helper)
void ProbeCopy(int* p, const int* v)
{
    if (p)
        *p = *v;
}
```

### 0x4010c7 `ProbeGet@`

```cpp
// 0x4010C7: lazy initialiser. BBT moved the "not yet set" branch to 0x53879D.
ProbeStruct* ProbeGet()
{
    if (!g_probe.fn)
        g_probe.fn = ProbeTarget;
    return &g_probe;
}
```

### 0x4010da `ProbeIdentity@`

```cpp
// 0x4010DA: mov eax,[esp+4] / ret 4
int __stdcall ProbeIdentity(int a)
{
    return a;
}
```

## Full original file (reference only, not compiled)

```cpp
// Probe.cpp - first experiments for the Zoo Tycoon toolchain.
// These reproduce three tiny functions from zoo.exe (addresses in Notes\zoo.map).
// Names are placeholders until we know what the real functions are.

struct ProbeStruct { int a, b, c; void (*fn)(); };

void ProbeTarget();                 // 0x441880 in the original
ProbeStruct g_probe;                // 0x638148 in the original

// 0x4010C7: lazy initialiser. BBT moved the "not yet set" branch to 0x53879D.
ProbeStruct* ProbeGet()
{
    if (!g_probe.fn)
        g_probe.fn = ProbeTarget;
    return &g_probe;
}

// 0x4010DA: mov eax,[esp+4] / ret 4
int __stdcall ProbeIdentity(int a)
{
    return a;
}

// 0x4010B6: copy-construct an int in place (looks like an STL construct() helper)
void ProbeCopy(int* p, const int* v)
{
    if (p)
        *p = *v;
}
```
