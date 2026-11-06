# Removed: Src/reg/static_globals6.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals6.cpp - class-static std::list<int>: guarded destructor (guard bit, clear, free header).
// Shapes 0x5823a5 and copies. Keep the file unchanged once an instance list refers to its symbols.
#include <list>

struct ProbeStatics6 {
    static std::list<int> s_list;
};
std::list<int> ProbeStatics6::s_list;
```
