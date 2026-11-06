# Removed: Src/misc/flagname.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: one-letter method names: f
- formatting: 5 packed + 0 overlong lines of 26
- readability: macro-stamped function family FLAGNAME

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (6)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x4269de | `?f@Z_4269DE@@QAEXXZ` | matched (zoo.map) |
| 0x50da26 | `?f@Z_50DA26@@QAEXXZ` | matched (zoo.map) |
| 0x52d018 | `?f@Z_52D018@@QAEXXZ` | matched (zoo.map) |
| 0x52d276 | `?f@Z_52D276@@QAEXXZ` | matched (zoo.map) |
| 0x52d9c4 | `?f@Z_52D9C4@@QAEXXZ` | matched (zoo.map) |
| 0x58a85e | `?f@Z_58A85E@@QAEXXZ` | matched (zoo.map) |

## Matching source per function

### 0x4269de `?f@Z_4269DE@@QAEXXZ`

```cpp
FLAGNAME(Z_4269DE, "bClean")
```

### 0x50da26 `?f@Z_50DA26@@QAEXXZ`

```cpp
FLAGNAME(Z_50DA26, "bFireWeapon")
```

### 0x52d018 `?f@Z_52D018@@QAEXXZ`

```cpp
FLAGNAME(Z_52D018, "bSweep")
```

### 0x52d276 `?f@Z_52D276@@QAEXXZ`

```cpp
FLAGNAME(Z_52D276, "bEmpty")
```

### 0x52d9c4 `?f@Z_52D9C4@@QAEXXZ`

```cpp
FLAGNAME(Z_52D9C4, "bEatStanding")
```

### 0x58a85e `?f@Z_58A85E@@QAEXXZ`

```cpp
FLAGNAME(Z_58A85E, "bSpeak")
```

## Full original file (reference only, not compiled)

```cpp
// flagname.cpp - "unless my owner's current name is X, call virtual 0x48(true)" (6 classes, each with
// its own literal; cluster 0x4269de). Names are placeholders Z_<address>.
#include <string>

typedef _STL::string String;

struct FN_Owner { char pad[0x54]; String m_name; };

struct FN_Base {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1C();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2C();
    virtual void v30(); virtual void v34(); virtual void v38(); virtual void v3C();
    virtual void v40(); virtual void v44();
    virtual void v48(bool on);
    int m_04, m_08, m_0C, m_10;
    FN_Owner* m_owner;                                      // +0x14
};

#define FLAGNAME(cls, text)                                                     \
    struct cls : FN_Base { void f(); };                                         \
    void cls::f()                                                               \
    {                                                                           \
        if (m_owner->m_name != text)                                            \
            v48(true);                                                          \
    }

FLAGNAME(Z_4269DE, "bClean")
FLAGNAME(Z_50DA26, "bFireWeapon")
FLAGNAME(Z_52D018, "bSweep")
FLAGNAME(Z_52D276, "bEmpty")
FLAGNAME(Z_52D9C4, "bEatStanding")
FLAGNAME(Z_58A85E, "bSpeak")
```
