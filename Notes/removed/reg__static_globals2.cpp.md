# Removed: Src/reg/static_globals2.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals2.cpp - reference translation unit for namespace-scope STLport containers (no guard
// byte, unlike the class statics in static_globals.cpp): their dynamic initialisers and destructors
// repeat once per global in zoo.exe (Notes/instances_globals2.csv).
#include <list>
#include <map>
#include <set>

std::map<int, int> g_probeMap;                       // ~map: clear + free header (0x58276D x11)
std::list<int> g_probeList;                          // list(): header node from the node allocator (0x55281E x6)
static std::map<int, int> s_probeMap;
static std::list<int> s_probeList;
std::set<int> g_probeSet;

int useStatics() { return s_probeMap.size() + s_probeList.size(); }
```
