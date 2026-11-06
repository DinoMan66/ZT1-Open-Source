# Removed: Src/stl/stl_map.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_map.cpp - explicit instantiations of STLport 4.0 map / set.
#include <map>
#include <set>
#include <string>
template class _STL::map<int, int>;
template class _STL::map<int, void*>;
template class _STL::map<_STL::string, int>;
template class _STL::map<_STL::string, void*>;
template class _STL::map<_STL::string, _STL::string>;
template class _STL::set<int>;
template class _STL::set<void*>;
template class _STL::set<_STL::string>;
```
