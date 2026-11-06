# Removed: Src/stl/stl_vector.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_vector.cpp - explicit instantiations of STLport 4.0 vector for common element types.
#include <vector>
#include <string>
struct Pod8 { int a, b; };
struct Pod12 { int a, b, c; };
struct Pod16 { int a, b, c, d; };
template class _STL::vector<int>;
template class _STL::vector<void*>;
template class _STL::vector<char>;
template class _STL::vector<short>;
template class _STL::vector<float>;
template class _STL::vector<double>;
template class _STL::vector<Pod8>;
template class _STL::vector<Pod12>;
template class _STL::vector<Pod16>;
template class _STL::vector<_STL::string>;
```
