# Removed: Src/reg/static_globals11.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals11.cpp - namespace-scope UIColor constants and a default-constructed UIColor[6]
// ($E1 green 0x53967f, $E2 red 0x5396a7, $E3 0x557ccf/0x573af6, $E4 array 0x558fda/0x55951c).
// Keep unchanged once Notes/instances_globals11.csv refers to its $E names.
typedef unsigned char BYTE;
struct UIColor
{
    UIColor() : c0(0), c1(0), c2(0) {}
    UIColor(BYTE a, BYTE b, BYTE c) : c0(a), c1(b), c2(c) {}
    BYTE c0, c1, c2;
};
UIColor g_63e9e9(0, 255, 0);
UIColor g_63e9e4(255, 0, 0);
UIColor g_63ba04(0x53, 0xdb, 0x53);
UIColor g_643418[6];
```
