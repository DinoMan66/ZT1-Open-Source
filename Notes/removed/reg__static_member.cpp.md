# Removed: Src/reg/static_member.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
#include <string>
struct Names { static const std::string kOverlay; };
const std::string Names::kOverlay("Overlay");
```
