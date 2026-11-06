# Removed: Src/reg/static_globals5.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals5.cpp - global containers wrapped in small classes whose destructors clear them first
// (0x582711 and 5 copies: `call clear; ~_Rb_tree inline`). Notes/instances_globals5.csv.
#include <map>
#include <list>
#include <vector>
#include <string>

struct G5MapDerived : std::map<int, std::string> { ~G5MapDerived() { clear(); } };
struct G5MapMember { std::map<int, std::string> m; ~G5MapMember() { m.clear(); } };
struct G5MapIntDerived : std::map<int, int> { ~G5MapIntDerived() { clear(); } };
struct G5MapIntMember { std::map<int, int> m; ~G5MapIntMember() { m.clear(); } };
struct G5ListDerived : std::list<int> { ~G5ListDerived() { clear(); } };
struct G5VecDerived : std::vector<int> { ~G5VecDerived() { clear(); } };
struct G5MapStrDerived : std::map<std::string, int> { ~G5MapStrDerived() { clear(); } };

G5MapDerived g5_a;
G5MapMember g5_b;
G5MapIntDerived g5_c;
G5MapIntMember g5_d;
G5ListDerived g5_e;
G5VecDerived g5_f;
G5MapStrDerived g5_g;
```
