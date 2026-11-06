# Removed: Src/reg/static_globals.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals.cpp - reference translation unit for the dynamic initialisers of class-static
// STLport containers that zoo.exe repeats (one per object; guarded destructors, MATCHING_NOTES 21):
//   s_vector  three zero stores + atexit(guarded destructor)   (Notes/instances_globals.csv)
//   s_map     _Rb_tree header node from the node allocator
//   s_string  8-byte default buffer
// Keep the file unchanged; the instance list refers to the symbols it produces.
#include <vector>
#include <map>
#include <string>

struct ProbeStatics {
    static std::vector<int> s_vector;
    static std::map<int, int> s_map;
    static std::string s_string;
};
std::vector<int> ProbeStatics::s_vector;
std::map<int, int> ProbeStatics::s_map;
std::string ProbeStatics::s_string;
```
