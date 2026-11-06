# Removed: Src/misc/strreturn.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: macro-stamped function family RETURN_CSTRING

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// strreturn.cpp - functions that return a std::string copy of a global C string (6 copies in two
// translation units; names are placeholders Z_<address>).
#include <string>

#define RETURN_CSTRING(name, global)                                            \
    extern const char* global;                                                  \
    _STL::string name()                                                         \
    {                                                                           \
        return global;                                                          \
    }
RETURN_CSTRING(Z_5FE02D, g_63b3c4)
RETURN_CSTRING(Z_5FE0A9, g_63b3b8)
RETURN_CSTRING(Z_5FE125, g_63b3b4)
RETURN_CSTRING(Z_624944, g_6538fc)
RETURN_CSTRING(Z_6249C0, g_6538ec)
RETURN_CSTRING(Z_624A3C, g_653910)
```
