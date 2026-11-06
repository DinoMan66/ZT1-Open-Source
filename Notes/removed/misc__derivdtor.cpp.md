# Removed: Src/misc/derivdtor.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 2, e.g. Z_4E0996, Z_5017CE

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (3)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x501860 | `??_GZ_501860@@UAEPAXI@Z` | matched (zoo.map) |
| 0x50295e | `??_GZ_50295E@@UAEPAXI@Z` | matched (zoo.map) |
| 0x503054 | `??_GZ_503054@@UAEPAXI@Z` | matched (zoo.map) |

## Matching source per function

### 0x501860 `??_GZ_501860@@UAEPAXI@Z`

```cpp
DERIVDTOR(Z_501860, Z_5017CE)
```

### 0x50295e `??_GZ_50295E@@UAEPAXI@Z`

```cpp
DERIVDTOR(Z_50295E, Z_4E0996)
```

### 0x503054 `??_GZ_503054@@UAEPAXI@Z`

```cpp
DERIVDTOR(Z_503054, Z_4E0996)
```

## Full original file (reference only, not compiled)

```cpp
// derivdtor.cpp - classes that add nothing to destroy: the scalar deleting destructor sets the vtable,
// calls the base destructor out of line, then frees (clusters 0x501860 / 0x50295e / 0x503054).
// The destructor is inline (written in the class), so it is folded into ??_G. An out-of-line ctor
// makes the vtable and ??_G appear here (genshapes also scores ??0 against the dtor address: ignore).
struct Z_5017CE { Z_5017CE(); virtual ~Z_5017CE(); };
struct Z_4E0996 { Z_4E0996(); virtual ~Z_4E0996(); };

#define DERIVDTOR(cls, base) struct cls : base { cls(); virtual ~cls() {} }; cls::cls() {}
DERIVDTOR(Z_501860, Z_5017CE)
DERIVDTOR(Z_50295E, Z_4E0996)
DERIVDTOR(Z_503054, Z_4E0996)
```
