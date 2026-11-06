# Removed: Src/reg/stl_inst6.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- formatting: 12 packed + 0 overlong lines of 26

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_inst6.cpp - out-of-line STLport members for string-keyed trees and friends, instantiated by use
// (Tools/shapescan.py, Notes/instances_stl6.csv). Keep unchanged once the list refers to its symbols.
#include <map>
#include <set>
#include <list>
#include <vector>
#include <string>

typedef std::string S;
void use6(std::map<S, int>& a, std::map<S, S>& b, std::set<S>& c, std::map<S, void*>& d,
          std::map<S, std::vector<int> >& e, std::map<int, S>& f, std::map<int, void*>& g,
          std::set<int>& h, std::set<void*>& i, std::map<int, std::vector<int> >& j,
          std::list<S>& k, std::vector<S>& l, std::map<S, float>& m, std::map<unsigned, int>& n)
{
    a[S("x")] = 1; a.insert(std::make_pair(S("y"), 2)); a.erase(S("x")); a.find(S("z"));
    b[S("x")] = S("y"); b.erase(S("x")); b.find(S("z"));
    c.insert(S("x")); c.erase(S("x")); c.find(S("z"));
    d[S("x")] = 0; d.erase(S("x")); d.find(S("z"));
    e[S("x")].push_back(1); e.erase(S("x"));
    f[1] = S("x"); f.erase(1); f.find(2);
    g[1] = 0; g.erase(1); g.find(2);
    h.insert(1); h.erase(1); h.find(2);
    i.insert((void*)0); i.erase((void*)0); i.find((void*)0);
    j[1].push_back(2); j.erase(1);
    k.push_back(S("x")); k.remove(S("x")); k.clear();
    l.push_back(S("x")); l.erase(l.begin()); l.clear();
    m[S("x")] = 1.0f; m.erase(S("x")); m.find(S("y"));
    n[1u] = 2; n.erase(1u); n.find(2u);
}
```
