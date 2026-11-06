# Removed: Src/misc/gridcheck.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- readability: macro-stamped function family GRID_CHECK

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (4)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x613426 | `?Z_613426@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z` | matched (zoo.map) |
| 0x61349c | `?Z_61349C@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z` | matched (zoo.map) |
| 0x618e3d | `?Z_618E3D@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z` | matched (zoo.map) |
| 0x618eb3 | `?Z_618EB3@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z` | matched (zoo.map) |

## Matching source per function

### 0x613426 `?Z_613426@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z`

```cpp
GRID_CHECK(Z_613426, g_63afc8)
```

### 0x61349c `?Z_61349C@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z`

```cpp
GRID_CHECK(Z_61349C, g_6463a0)
```

### 0x618e3d `?Z_618E3D@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z`

```cpp
GRID_CHECK(Z_618E3D, g_63c518)
```

### 0x618eb3 `?Z_618EB3@@YA_NPAUZTGrid4@@PAUZTGridPoint@@@Z`

```cpp
GRID_CHECK(Z_618EB3, g_63c508)
```

## Full original file (reference only, not compiled)

```cpp
// gridcheck.cpp - "is the animal in quarter-cell <p> of this 64x64 block one that passes test <X>?"
// 4 copies that differ only in the test descriptor (cluster 0x613426). Names are placeholders Z_<address>.
#include "../include/ztaction.h"

struct ZTGridPoint { int x, y; };
struct ZTGrid4 { int m_unk00; ZTEntity* m_cells[2][2]; };
extern char g_638680;
bool f41239d(ZTEntity* e, void* test, int a);

#define GRID_CHECK(name, test)                                                  \
    extern char test;                                                           \
    bool name(ZTGrid4* g, ZTGridPoint* p)                                       \
    {                                                                           \
        bool r = false;                                                         \
        if (g && p->x >= 0 && p->y >= 0 && p->x < 64 && p->y < 64) {            \
            ZTEntity* e = g->m_cells[p->x / 32][p->y / 32];                     \
            if (e && e->m_type->isKindOf(&g_638680))                            \
                r = f41239d(e, &test, 0);                                       \
        }                                                                       \
        return r;                                                               \
    }
GRID_CHECK(Z_613426, g_63afc8)
GRID_CHECK(Z_61349C, g_6463a0)
GRID_CHECK(Z_618E3D, g_63c518)
GRID_CHECK(Z_618EB3, g_63c508)
```
