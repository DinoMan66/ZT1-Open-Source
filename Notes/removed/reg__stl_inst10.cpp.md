# Removed: Src/reg/stl_inst10.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- formatting: 13 packed + 0 overlong lines of 32

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_inst10.cpp - more STLport members (hash containers, adaptors, less common members), instantiated
// by use; Tools/shapescan.py -> Notes/instances_stl10.csv. Keep unchanged once listed.
#include <hash_map>
#include <hash_set>
#include <map>
#include <set>
#include <list>
#include <vector>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <algorithm>

void use10(std::hash_map<int, int>& a, std::hash_map<std::string, int>& b, std::hash_set<int>& c,
           std::priority_queue<int>& d, std::stack<int>& e, std::queue<int>& f,
           std::map<int, int>& g, std::set<int>& h, std::list<int>& i, std::list<int>& i2,
           std::vector<int>& j, std::multimap<int, int>& k, std::map<std::string, int>& l,
           std::vector<void*>& m, std::list<void*>& n, std::set<std::string>& o)
{
    a[1] = 2; a.erase(1); a.find(2); a.clear();
    b[std::string("x")] = 1; b.erase(std::string("x")); b.find(std::string("y")); b.clear();
    c.insert(1); c.erase(1); c.find(2); c.clear();
    d.push(1); d.pop(); e.push(1); e.pop(); f.push(1); f.pop();
    g.lower_bound(1); g.upper_bound(1); g.equal_range(1); g.count(1); g.erase(g.begin(), g.end());
    h.lower_bound(1); h.upper_bound(1); h.count(1); h.erase(h.begin(), h.end());
    i.splice(i.begin(), i2); i.merge(i2); i.unique(); i.reverse(); i.remove(3); i.sort(); i.resize(4);
    j.assign(5, 1); j.insert(j.end(), i.begin(), i.end()); std::reverse(j.begin(), j.end());
    std::stable_sort(j.begin(), j.end()); std::unique(j.begin(), j.end()); std::remove(j.begin(), j.end(), 1);
    k.insert(std::make_pair(1, 2)); k.erase(1); k.count(1); k.equal_range(1);
    l.lower_bound(std::string("a")); l.count(std::string("a")); l.erase(l.begin(), l.end());
    m.erase(std::remove(m.begin(), m.end(), (void*)0), m.end()); std::sort(m.begin(), m.end());
    n.remove((void*)0); n.sort(); n.unique();
    o.lower_bound(std::string("a")); o.count(std::string("a")); o.erase(o.begin(), o.end());
}
```
