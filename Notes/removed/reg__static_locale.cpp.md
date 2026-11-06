# Removed: Src/reg/static_locale.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_locale.cpp - reference translation unit: a game .cpp that includes <locale> (through STLport 4.0,
// which pulls in the native VC6 locale templates). The template statics collate<char>::id and
// ctype<unsigned short>::id get one shared guard each (0x64A6E8 / 0x64A6E9) and an atexit for their
// empty destructor in EVERY such translation unit. Notes/instances_static_init.csv shape "locale-ids".
// Keep this file unchanged: the list refers to its $E symbol numbers.
#include <string>
#include <locale>
static const std::string kFood("food");
```
