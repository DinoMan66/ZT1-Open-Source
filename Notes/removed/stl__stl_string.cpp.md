# Removed: Src/stl/stl_string.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_string.cpp - explicit instantiation of STLport 4.0 basic_string<char> to identify the string
// member functions zoo.exe links in (Tools/shapescan.py --all). Not a game translation unit.
#include <string>
template class _STL::basic_string<char>;
```
