# Removed: Src/misc/lookup2.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: one-letter method names: f
- readability: macro-stamped function family TABLE_GET

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (4)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x592632 | `?f@Z_592632@@QAEHXZ` | matched (zoo.map) |
| 0x592659 | `?f@Z_592659@@QAEHXZ` | matched (zoo.map) |
| 0x592680 | `?f@Z_592680@@QAEHXZ` | matched (zoo.map) |
| 0x5926a7 | `?f@Z_5926A7@@QAEHXZ` | matched (zoo.map) |

## Matching source per function

### 0x592632 `?f@Z_592632@@QAEHXZ`

```cpp
TABLE_GET(Z_592632, g_6418e8, g_641890)
```

### 0x592659 `?f@Z_592659@@QAEHXZ`

```cpp
TABLE_GET(Z_592659, g_6418fc, g_64187c)
```

### 0x592680 `?f@Z_592680@@QAEHXZ`

```cpp
TABLE_GET(Z_592680, g_6418c8, g_6418a4)
```

### 0x5926a7 `?f@Z_5926A7@@QAEHXZ`

```cpp
TABLE_GET(Z_5926A7, g_6418d8, g_6418b4)
```

## Full original file (reference only, not compiled)

```cpp
// lookup2.cpp - getters that look a value up in a two-key table member (+0x18), falling back to a global
// default (cluster 0x592632 x4; table lookup 0x4098C1). Names are placeholders Z_<address>.
struct ZTTable2 { bool m4098c1(int key1, int key2, int* out); };
extern int g_6418c4;

#define TABLE_GET(cls, def, key2)                                               \
    extern int def, key2;                                                       \
    struct cls { unsigned char m_unk00[0x18]; ZTTable2 m_table; int f(); };     \
    int cls::f()                                                                \
    {                                                                           \
        int v = def;                                                            \
        m_table.m4098c1(g_6418c4, key2, &v);                                    \
        return v;                                                               \
    }
TABLE_GET(Z_592632, g_6418e8, g_641890)
TABLE_GET(Z_592659, g_6418fc, g_64187c)
TABLE_GET(Z_592680, g_6418c8, g_6418a4)
TABLE_GET(Z_5926A7, g_6418d8, g_6418b4)
```
