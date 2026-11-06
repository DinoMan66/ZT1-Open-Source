# Removed: Src/stl/stl_more.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_more.cpp - more STLport 4.0 instantiations: deque, hash_map, algorithms on vectors.
#include <deque>
#include <hash_map>
#include <vector>
#include <algorithm>
#include <string>
template class _STL::deque<int>;
template class _STL::deque<void*>;
template class _STL::hash_map<int, int>;
template class _STL::hash_map<int, void*>;
void sortInts(_STL::vector<int>& v) { _STL::sort(v.begin(), v.end()); }
void sortPtrs(_STL::vector<void*>& v) { _STL::sort(v.begin(), v.end()); }
void sortFloats(_STL::vector<float>& v) { _STL::sort(v.begin(), v.end()); }
int* findInt(_STL::vector<int>& v, int x) { return _STL::find(v.begin(), v.end(), x); }
void** findPtr(_STL::vector<void*>& v, void* x) { return _STL::find(v.begin(), v.end(), x); }
```
