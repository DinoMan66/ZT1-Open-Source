# Removed: Src/reg/static_globals3.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals3.cpp - more namespace-scope STLport containers whose initialisers / destructors repeat
// per global in zoo.exe (shapes found with Tools/shapescan.py, Notes/instances_globals3.csv).
// Keep the file unchanged once the list refers to its $E symbols.
#include <list>
#include <map>
#include <set>
#include <vector>
#include <deque>
#include <string>

std::vector<int> g3_vecInt;
std::vector<std::string> g3_vecStr;
std::set<int> g3_setInt;
std::set<void*> g3_setPtr;
std::map<int, std::string> g3_mapIntStr;
std::map<std::string, int> g3_mapStrInt;
std::map<int, void*> g3_mapIntPtr;
std::list<std::string> g3_listStr;
std::list<void*> g3_listPtr;
std::deque<int> g3_dequeInt;
std::map<std::string, std::string> g3_mapStrStr;
std::multimap<int, int> g3_multimap;
```
