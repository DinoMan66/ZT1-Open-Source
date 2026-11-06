# Removed: Src/reg/static_globals9.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals9.cpp - probe: a namespace-scope object holding std::map<int, std::set<int> > whose inline
// ctor and dtor both call an out-of-line reset() (0x40A5BC): $E1 ctor 0x55248c x3, $E2 dtor 0x582711 x3.
// Keep unchanged: Notes/instances_globals9.csv keys on _$E1/_$E2.
#include <map>
#include <set>

struct ZTIdSets
{
    std::map<int, std::set<int> > m_sets;
    ZTIdSets() { reset(); }
    ~ZTIdSets() { reset(); }
    void reset();
};
ZTIdSets g_641840;
```
