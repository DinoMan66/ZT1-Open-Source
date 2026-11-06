# Removed: Src/reg/static_globals4.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals4.cpp - further namespace-scope container shapes (see static_globals3.cpp,
// Notes/instances_globals4.csv). Keep unchanged once the list refers to its symbols.
#include <list>
#include <map>
#include <set>
#include <vector>
#include <string>

std::map<int, double> g4_mapIntDouble;
std::map<int, std::pair<int, int> > g4_mapIntPair;
std::set<std::string> g4_setStr;
std::list<std::pair<int, int> > g4_listPair;
std::vector<std::pair<int, int> > g4_vecPair;
std::map<int, std::vector<int> > g4_mapIntVec;
std::map<std::string, std::vector<int> > g4_mapStrVec;
std::map<int, std::list<int> > g4_mapIntList;
std::list<std::vector<int> > g4_listVec;
std::set<std::pair<int, int> > g4_setPair;
std::map<std::string, void*> g4_mapStrPtr;
std::vector<std::vector<int> > g4_vecVec;
std::map<int, std::map<int, int> > g4_mapMap;
std::list<int> g4_listInt;
std::map<void*, int> g4_mapPtrInt;
```
