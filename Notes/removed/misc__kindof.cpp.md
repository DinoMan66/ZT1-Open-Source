# Removed: Src/misc/kindof.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 1, e.g. K_40FB6A
- readability: macro-stamped function family KINDOF

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (12)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x40f80a | `?isKindOf@K_40F80A@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40f821 | `?isKindOf@K_40F821@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40f856 | `?isKindOf@K_40F856@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40f982 | `?isKindOf@K_40F982@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40f9a9 | `?isKindOf@K_40F9A9@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40fb6a | `?isKindOf@K_40FB6A@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40fbd6 | `?isKindOf@K_40FBD6@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40fd7f | `?isKindOf@K_40FD7F@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40fdd6 | `?isKindOf@K_40FDD6@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x40feca | `?isKindOf@K_40FECA@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x41113b | `?isKindOf@K_41113B@@QAE_NPBX@Z` | matched (zoo.map) |
| 0x5b0ebb | `?isKindOf@K_5B0EBB@@QAE_NPBX@Z` | matched (zoo.map) |

## Matching source per function

### 0x40f80a `?isKindOf@K_40F80A@@QAE_NPBX@Z`

```cpp
KINDOF(K_40F80A, K_40F821, g_638660)
```

### 0x40f821 `?isKindOf@K_40F821@@QAE_NPBX@Z`

```cpp
KINDOF(K_40F821, K_40FB6A, g_638670)
```

### 0x40f856 `?isKindOf@K_40F856@@QAE_NPBX@Z`

```cpp
KINDOF(K_40F856, K_40F821, g_638680)
```

### 0x40f982 `?isKindOf@K_40F982@@QAE_NPBX@Z`

```cpp
KINDOF(K_40F982, K_40FBD6, g_6386b0)
```

### 0x40f9a9 `?isKindOf@K_40F9A9@@QAE_NPBX@Z`

```cpp
KINDOF(K_40F9A9, K_40F821, g_6386a0)
```

### 0x40fb6a `?isKindOf@K_40FB6A@@QAE_NPBX@Z`

```cpp
struct K_40FB6A {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C();
    virtual void v10();
    virtual const String& type() const;                     // slot 0x14
    bool isKindOf(const void* id);
};

bool K_40FB6A::isKindOf(const void* id)
{
    return &type() == id;
}
```

### 0x40fbd6 `?isKindOf@K_40FBD6@@QAE_NPBX@Z`

```cpp
KINDOF(K_40FBD6, K_40FB6A, g_6386b0)
```

### 0x40fd7f `?isKindOf@K_40FD7F@@QAE_NPBX@Z`

```cpp
KINDOF(K_40FD7F, K_40FDD6, g_638740)
```

### 0x40fdd6 `?isKindOf@K_40FDD6@@QAE_NPBX@Z`

```cpp
KINDOF(K_40FDD6, K_40FB6A, g_638750)
```

### 0x40feca `?isKindOf@K_40FECA@@QAE_NPBX@Z`

```cpp
KINDOF(K_40FECA, K_40F821, g_6386c0)
```

### 0x41113b `?isKindOf@K_41113B@@QAE_NPBX@Z`

```cpp
KINDOF(K_41113B, K_40F821, g_6387a0)
```

### 0x5b0ebb `?isKindOf@K_5B0EBB@@QAE_NPBX@Z`

```cpp
KINDOF(K_5B0EBB, K_40F821, g_639100)
```

## Full original file (reference only, not compiled)

```cpp
// kindof.cpp - the pointer form of the run-time type test (cf. isa.cpp): isKindOf(id) compares the
// address of a class's type-name string, then asks the base; the root compares &type().
// BBT inlined the root and first-level bodies into their callers, so the chain lives in one object.
#include <string>

typedef _STL::string String;

struct K_40FB6A {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C();
    virtual void v10();
    virtual const String& type() const;                     // slot 0x14
    bool isKindOf(const void* id);
};
bool K_40FB6A::isKindOf(const void* id)
{
    return &type() == id;
}

#define KINDOF(cls, base, str)                                                  \
    extern const String str;                                                    \
    struct cls : base { bool isKindOf(const void* id); };                       \
    bool cls::isKindOf(const void* id)                                          \
    {                                                                           \
        return id == &str || base::isKindOf(id);                                \
    }

KINDOF(K_40FBD6, K_40FB6A, g_6386b0)
KINDOF(K_40F821, K_40FB6A, g_638670)
KINDOF(K_40FDD6, K_40FB6A, g_638750)
KINDOF(K_40F982, K_40FBD6, g_6386b0)
KINDOF(K_40F856, K_40F821, g_638680)
KINDOF(K_40F9A9, K_40F821, g_6386a0)
KINDOF(K_40FECA, K_40F821, g_6386c0)
KINDOF(K_41113B, K_40F821, g_6387a0)
KINDOF(K_5B0EBB, K_40F821, g_639100)
KINDOF(K_40F80A, K_40F821, g_638660)
KINDOF(K_40FD7F, K_40FDD6, g_638740)
```
