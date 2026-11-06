# Removed: Src/reg/static_misc.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_misc.cpp - reference translation unit for more compiler-generated code that zoo.exe repeats:
//   ??_GProbeVirtual@@  scalar deleting destructor (every class with a virtual destructor defined in a TU)
//   ?idleName@@         function-local static std::string returned by reference (guard bit + atexit)
// Notes/instances_misc.csv refers to these symbols; keep the file unchanged.
#include <string>

struct ProbeVirtual {
    virtual ~ProbeVirtual();
    int m_value;
};
ProbeVirtual::~ProbeVirtual() { m_value = 0; }
void probeDelete(ProbeVirtual* p) { delete p; }

const std::string& idleName()
{
    static std::string s_name("idle");
    return s_name;
}
```
