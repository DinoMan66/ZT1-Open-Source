# Removed: Src/reg/static_globals12.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals12.cpp - namespace-scope arrays of three std::map (node 0x18 / 0x20): the $E constructs
// all three in a loop (clusters 0x56c8a3 / 0x56c8f7). Keep unchanged once an instances list refers to it.
#include <map>

struct ZTRec12 { int a, b, c; };
std::map<int, ZTRec12> g_64ebb0[3];
std::map<int, int> g_64eb88[3];
```
