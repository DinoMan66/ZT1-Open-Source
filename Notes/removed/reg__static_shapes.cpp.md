# Removed: Src/reg/static_shapes.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- depends on: 

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_shapes.cpp - reference translation unit for the compiler-generated static-initialisation
// code that zoo.exe repeats in nearly every translation unit (Notes/instances_static_init.csv,
// checked with Tools/instances.py). Keep this file exactly as it is: instances_static_init.csv
// refers to its $E symbol numbers.
//   _$E14 string-ctor   inlined basic_string(const char*) into a file-static global
//   _$E15 string-dtor   the atexit destructor of that global
//   _$E16 atexit-stub   atexit(_$E15)
//   _$E17 init-wrapper  call _$E14 / jmp _$E16 (BBT laid _$E16 right behind it)
// The header these come from (13 need/building names: food, drink, bathroom, gift, trash, fun,
// energy, eat, animalrest, building, grandstand, showtrick, fungift) is not identified yet.
#include <string>
static const std::string kFunGift("fungift");
static const std::string kFood("food");
```
