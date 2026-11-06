# Removed: Src/reg/static_globals7.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals7.cpp - probe: namespace-scope const string reference bound to a temporary built from a
// char array (cluster 0x57a9e3 x5: one $E fills the temporary and stores the reference). Keep unchanged:
// Notes/instances_globals7.csv keys on _$E14.
#include <string>

extern const char g_63ba4c[];
const std::string& g_63950c = std::string(g_63ba4c);
```
