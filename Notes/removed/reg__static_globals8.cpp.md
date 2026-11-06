# Removed: Src/reg/static_globals8.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: verification scaffolding (probe / reference unit / instantiation driver), not game code

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// static_globals8.cpp - namespace-scope objects whose class has an out-of-line constructor and no
// destructor: the $E is `mov ecx,offset g / jmp ctor` (cluster 0x57b2e5, ctor 0x40E420 = UIScrollBarPart).
// Keep unchanged once Notes/instances_globals8.csv refers to its $E names.
class UIScrollBarPart
{
public:
    UIScrollBarPart();
    unsigned char m_data[0x68];
};
UIScrollBarPart g_6430e8;
```
