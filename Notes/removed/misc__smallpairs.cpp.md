# Removed: Src/misc/smallpairs.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 2, e.g. Z_4435B9, Z_620299
- descriptive names: one-letter method names: f
- formatting: 31 packed + 0 overlong lines of 154
- readability: macro-stamped function family FWD_EMBEDDED

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (46)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x41028c | `?f@Z_41028C@@QAEX_NH@Z` | matched (zoo.map) |
| 0x410e20 | `?Z_410E20@@YAPAUZTKind@@PAU1@@Z` | matched (zoo.map) |
| 0x410e5c | `?Z_410E5C@@YAPAUZTKind@@PAU1@@Z` | matched (zoo.map) |
| 0x4131f9 | `?f@Z_4131F9@@QAEXXZ` | matched (zoo.map) |
| 0x413304 | `?f@Z_413304@@QAEXXZ` | matched (zoo.map) |
| 0x413aa7 | `?Z_413AA7@@YGPAUZTObj413A87@@HH@Z` | matched (zoo.map) |
| 0x413bec | `?Z_413BEC@@YGPAUZTObj413BA8@@HH@Z` | matched (zoo.map) |
| 0x42aa0a | `?f@Z_42AA0A@@QAEXD@Z` | matched (zoo.map) |
| 0x42dca9 | `?Z_42DCA9@@YA_NH@Z` | matched (zoo.map) |
| 0x43d25e | `?f@Z_43D25E@@QAEXABUZTVec3@@@Z` | matched (zoo.map) |
| 0x43e8d3 | `?f@Z_43E8D3@@QAEXHH@Z` | matched (zoo.map) |
| 0x43e8f4 | `?f@Z_43E8F4@@QAEXXZ` | matched (zoo.map) |
| 0x43eacc | `?f@Z_43EACC@@QAEXXZ` | matched (zoo.map) |
| 0x43f0d5 | `?f@Z_43F0D5@@QAEXD@Z` | matched (zoo.map) |
| 0x4435b9 | `?f@Z_4435B9@@QAEHHHH@Z` | matched (zoo.map) |
| 0x46ab65 | `?Z_46AB65@@YAXH@Z` | matched (zoo.map) |
| 0x4708ea | `?f@Z_4708EA@@QAEXH@Z` | matched (zoo.map) |
| 0x48bf55 | `?f@Z_48BF55@@QAEXABUZTVec3@@@Z` | matched (zoo.map) |
| 0x49a147 | `?f@Z_49A147@@QAE_NHH@Z` | matched (zoo.map) |
| 0x49ebce | `?f@Z_49EBCE@@QAEXH@Z` | matched (zoo.map) |
| 0x4a75a7 | `?f@Z_4A75A7@@QAE_NHH@Z` | matched (zoo.map) |
| 0x4a8a23 | `?f@Z_4A8A23@@QAEXH@Z` | matched (zoo.map) |
| 0x4b2355 | `?Z_4B2355@@YAXXZ` | matched (zoo.map) |
| 0x4d5dfe | `?f@Z_4D5DFE@@QAEXXZ` | matched (zoo.map) |
| 0x4d6f6b | `?f@Z_4D6F6B@@QAEXXZ` | matched (zoo.map) |
| 0x4d954a | `?f@Z_4D954A@@QAEXXZ` | matched (zoo.map) |
| 0x4d9573 | `?f@Z_4D9573@@QAEXXZ` | matched (zoo.map) |
| 0x4dbf90 | `?f@Z_4DBF90@@QAEXXZ` | matched (zoo.map) |
| 0x4ed80a | `?Z_4ED80A@@YAXXZ` | matched (zoo.map) |
| 0x512c87 | `?Z_512C87@@YAXH@Z` | matched (zoo.map) |
| 0x57db2e | `?Z_57DB2E@@YAXXZ` | matched (zoo.map) |
| 0x5acf8a | `?f@Z_5ACF8A@@QAEXXZ` | matched (zoo.map) |
| 0x5fdb38 | `?Z_5FDB38@@YAXHH@Z` | matched (zoo.map) |
| 0x600603 | `?Z_600603@@YAXXZ` | matched (zoo.map) |
| 0x6022c8 | `?f@Z_6022C8@@QAEXHH@Z` | matched (zoo.map) |
| 0x603fdd | `?f@Z_603FDD@@QAEXH@Z` | matched (zoo.map) |
| 0x603ff2 | `?f@Z_603FF2@@QAE?AUZTVec3@@XZ` | matched (zoo.map) |
| 0x604021 | `?f@Z_604021@@QAE?AUZTVec3@@XZ` | matched (zoo.map) |
| 0x604070 | `?f@Z_604070@@QAE?AUZTVec3@@XZ` | matched (zoo.map) |
| 0x611b31 | `?Z_611B31@@YA_NH@Z` | matched (zoo.map) |
| 0x612edb | `?f@Z_612EDB@@QAEHHHHH@Z` | matched (zoo.map) |
| 0x615b1a | `?f@Z_615B1A@@QAEX_NH@Z` | matched (zoo.map) |
| 0x618c8c | `?Z_618C8C@@YAXXZ` | matched (zoo.map) |
| 0x61b61d | `?f@Z_61B61D@@QAEHHHHH@Z` | matched (zoo.map) |
| 0x620299 | `?f@Z_620299@@QAEHHHH@Z` | matched (zoo.map) |
| 0x628ce6 | `?Z_628CE6@@YAXHH@Z` | matched (zoo.map) |

## Matching source per function

### 0x41028c `?f@Z_41028C@@QAEX_NH@Z`

```cpp
SET_144_134(Z_41028C)
```

### 0x410e20 `?Z_410E20@@YAPAUZTKind@@PAU1@@Z`

```cpp
CAST_TO(Z_410E20, g_638690)
CAST_TO(Z_410E5C, g_638660)

// ---- 82: delete a global manager (non-virtual out-of-line destructor)
#define DELETE_GLOBAL(name, cls, global)                                        \
    struct cls { ~cls(); }
```

### 0x410e5c `?Z_410E5C@@YAPAUZTKind@@PAU1@@Z`

```cpp
CAST_TO(Z_410E5C, g_638660)

// ---- 82: delete a global manager (non-virtual out-of-line destructor)
#define DELETE_GLOBAL(name, cls, global)                                        \
    struct cls { ~cls(); }
```

### 0x4131f9 `?f@Z_4131F9@@QAEXXZ`

```cpp
RESET_2(Z_4131F9, m41308d, m4131c8)
```

### 0x413304 `?f@Z_413304@@QAEXXZ`

```cpp
RESET_RUN(Z_413304)
```

### 0x413aa7 `?Z_413AA7@@YGPAUZTObj413A87@@HH@Z`

```cpp
CREATE2(Z_413AA7, ZTObj413A87)
CREATE2(Z_413BEC, ZTObj413BA8)

// ---- 67: return a 12-byte value produced by the member at +8
#define GET_VEC(cls, tcls, method)                                              \
    struct tcls { ZTVec3 method(); }
```

### 0x413bec `?Z_413BEC@@YGPAUZTObj413BA8@@HH@Z`

```cpp
CREATE2(Z_413BEC, ZTObj413BA8)

// ---- 67: return a 12-byte value produced by the member at +8
#define GET_VEC(cls, tcls, method)                                              \
    struct tcls { ZTVec3 method(); }
```

### 0x42aa0a `?f@Z_42AA0A@@QAEXD@Z`

```cpp
FLAG_13F(Z_42AA0A, f42a9fa)
```

### 0x42dca9 `?Z_42DCA9@@YA_NH@Z`

```cpp
bool Z_42DCA9(int id) { return id == g_63afe8; }
```

### 0x43d25e `?f@Z_43D25E@@QAEXABUZTVec3@@@Z`

```cpp
SET_POS(Z_43D25E, ZTT43D286, m43d286)
```

### 0x43e8d3 `?f@Z_43E8D3@@QAEXHH@Z`

```cpp
FWD_15C(Z_43E8D3)
```

### 0x43e8f4 `?f@Z_43E8F4@@QAEXXZ`

```cpp
RESET_2(Z_43E8F4, m41303c, m41300b)
```

### 0x43eacc `?f@Z_43EACC@@QAEXXZ`

```cpp
RESET_RUN(Z_43EACC)
```

### 0x43f0d5 `?f@Z_43F0D5@@QAEXD@Z`

```cpp
FLAG_13F(Z_43F0D5, f43f0c5)
```

### 0x4435b9 `?f@Z_4435B9@@QAEHHHH@Z`

```cpp
struct Z_4435B9 { void m4435a8(int a, int b, int c); int f(int a, int b, int c); };

int Z_4435B9::f(int a, int b, int c) { m4435a8(a, b, c); return 0; }
```

### 0x46ab65 `?Z_46AB65@@YAXH@Z`

```cpp
FWD_1(Z_46AB65, f46aa89)
FWD_1(Z_512C87, f512970)

// ---- 104 / 93 / 88: member forwards that keep `this` in ecx for the callee (thiscall, ecx untouched)
#define FWD2_1(cls, callee)                                                     \
    struct cls { bool callee(int a, int b, int c); bool f(int a, int b); }
```

### 0x4708ea `?f@Z_4708EA@@QAEXH@Z`

```cpp
FWD_8(Z_4708EA, ZTT41308D, m41308d)
```

### 0x48bf55 `?f@Z_48BF55@@QAEXABUZTVec3@@@Z`

```cpp
SET_POS(Z_48BF55, ZTT48BF7D, m48bf7d)
```

### 0x49a147 `?f@Z_49A147@@QAE_NHH@Z`

```cpp
FWD2_1(Z_49A147, m499886)
```

### 0x49ebce `?f@Z_49EBCE@@QAEXH@Z`

```cpp
FWD_COMPUTED(Z_49EBCE, m411285)
```

### 0x4a75a7 `?f@Z_4A75A7@@QAE_NHH@Z`

```cpp
FWD2_1(Z_4A75A7, m425533)
```

### 0x4a8a23 `?f@Z_4A8A23@@QAEXH@Z`

```cpp
FWD_COMPUTED(Z_4A8A23, m410349)
```

### 0x4b2355 `?Z_4B2355@@YAXXZ`

```cpp
void Z_4B2355() { ZTScreen4B2322* s = (ZTScreen4B2322*)UIH_4017E5(); if (s) s->m4b2322(0, 1); }
```

### 0x4d5dfe `?f@Z_4D5DFE@@QAEXXZ`

```cpp
ARM_RUN(Z_4D5DFE)
```

### 0x4d6f6b `?f@Z_4D6F6B@@QAEXXZ`

```cpp
ARM_RUN(Z_4D6F6B)
```

### 0x4d954a `?f@Z_4D954A@@QAEXXZ`

```cpp
FWD_EMBEDDED(Z_4D954A, 0x1e0)
```

### 0x4d9573 `?f@Z_4D9573@@QAEXXZ`

```cpp
FWD_EMBEDDED(Z_4D9573, 0x1e8)
```

### 0x4dbf90 `?f@Z_4DBF90@@QAEXXZ`

```cpp
FWD_EMBEDDED(Z_4DBF90, 0x1e0)
```

### 0x4ed80a `?Z_4ED80A@@YAXXZ`

```cpp
void Z_4ED80A() { ZTScreen4B2322* s = (ZTScreen4B2322*)UIH_4017E5(); if (s) s->m4b2322(0, 1); }
```

### 0x512c87 `?Z_512C87@@YAXH@Z`

```cpp
FWD_1(Z_512C87, f512970)

// ---- 104 / 93 / 88: member forwards that keep `this` in ecx for the callee (thiscall, ecx untouched)
#define FWD2_1(cls, callee)                                                     \
    struct cls { bool callee(int a, int b, int c); bool f(int a, int b); }
```

### 0x57db2e `?Z_57DB2E@@YAXXZ`

```cpp
DELETE_GLOBAL(Z_57DB2E, ZTMgr57DB55, g_638044)
DELETE_GLOBAL(Z_57DE67, ZTMgr57DE8E, g_638050)

// ---- 97: two-field setter
#define SET_144_134(cls)                                                        \
    struct cls { BYTE m_unk00[0x134]; int m_unk134; BYTE m_unk138[0x144 - 0x138]; bool m_unk144; \
                 void f(bool a, int b); }
```

### 0x5acf8a `?f@Z_5ACF8A@@QAEXXZ`

```cpp
FWD_EMBEDDED(Z_5ACF8A, 0x1e8)
```

### 0x5fdb38 `?Z_5FDB38@@YAXHH@Z`

```cpp
SET2(Z_5FDB38, g_6543a8, g_654398)
SET2(Z_628CE6, g_64c2c0, g_64c2c4)

// ---- 108: compare with a global id (same global in both copies)
extern int g_63afe8;
bool Z_42DCA9(int id) { return id == g_63afe8; }
```

### 0x600603 `?Z_600603@@YAXXZ`

```cpp
void Z_600603() { g_6390a8 = !g_6390a8; }
```

### 0x6022c8 `?f@Z_6022C8@@QAEXHH@Z`

```cpp
FWD_15C(Z_6022C8)
```

### 0x603fdd `?f@Z_603FDD@@QAEXH@Z`

```cpp
FWD_8(Z_603FDD, ZTT41303C, m41303c)
```

### 0x603ff2 `?f@Z_603FF2@@QAE?AUZTVec3@@XZ`

```cpp
GET_VEC(Z_603FF2, ZTT603433, m603433)
```

### 0x604021 `?f@Z_604021@@QAE?AUZTVec3@@XZ`

```cpp
GET_VEC(Z_604021, ZTT4971A9, m4971a9)
```

### 0x604070 `?f@Z_604070@@QAE?AUZTVec3@@XZ`

```cpp
GET_VEC(Z_604070, ZTT4993D7, m4993d7)
```

### 0x611b31 `?Z_611B31@@YA_NH@Z`

```cpp
bool Z_611B31(int id) { return id == g_63afe8; }
```

### 0x612edb `?f@Z_612EDB@@QAEHHHHH@Z`

```cpp
FWD4(Z_612EDB, m602307)
```

### 0x615b1a `?f@Z_615B1A@@QAEX_NH@Z`

```cpp
SET_144_134(Z_615B1A)
```

### 0x618c8c `?Z_618C8C@@YAXXZ`

```cpp
void Z_618C8C() { g_639357 = !g_639357; }
```

### 0x61b61d `?f@Z_61B61D@@QAEHHHHH@Z`

```cpp
FWD4(Z_61B61D, m610f8f)
```

### 0x620299 `?f@Z_620299@@QAEHHHH@Z`

```cpp
struct Z_620299 : Z_4435B9 { int f(int a, int b, int c); };

int Z_620299::f(int a, int b, int c) { Z_4435B9::f(a, b, c); return 0; }
```

### 0x628ce6 `?Z_628CE6@@YAXHH@Z`

```cpp
SET2(Z_628CE6, g_64c2c0, g_64c2c4)

// ---- 108: compare with a global id (same global in both copies)
extern int g_63afe8;
bool Z_42DCA9(int id) { return id == g_63afe8; }
```

## Full original file (reference only, not compiled)

```cpp
// smallpairs.cpp - small functions that occur two or three times with the same code (Notes/generated/clusters.md
// 67-114). Names are placeholders Z_<address>; callees not written yet are declared by address.
typedef unsigned char BYTE;

// ---- 83: checked downcast (slot 7 = isKindOf)
struct ZTKind { virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
                virtual void s5(); virtual void s6(); virtual bool isKindOf(const void* type); };
#define CAST_TO(name, type)                                                     \
    extern char type;                                                           \
    ZTKind* name(ZTKind* e)                                                     \
    {                                                                           \
        if (e && e->isKindOf(&type))                                            \
            return e;                                                           \
        return 0;                                                               \
    }
CAST_TO(Z_410E20, g_638690)
CAST_TO(Z_410E5C, g_638660)

// ---- 82: delete a global manager (non-virtual out-of-line destructor)
#define DELETE_GLOBAL(name, cls, global)                                        \
    struct cls { ~cls(); };                                                     \
    extern cls* global;                                                         \
    void name()                                                                 \
    {                                                                           \
        delete global;                                                          \
        global = 0;                                                             \
    }
DELETE_GLOBAL(Z_57DB2E, ZTMgr57DB55, g_638044)
DELETE_GLOBAL(Z_57DE67, ZTMgr57DE8E, g_638050)

// ---- 97: two-field setter
#define SET_144_134(cls)                                                        \
    struct cls { BYTE m_unk00[0x134]; int m_unk134; BYTE m_unk138[0x144 - 0x138]; bool m_unk144; \
                 void f(bool a, int b); };                                      \
    void cls::f(bool a, int b) { m_unk144 = a; m_unk134 = b; }
SET_144_134(Z_41028C)
SET_144_134(Z_615B1A)

// ---- 107: store two globals
#define SET2(name, ga, gb)                                                      \
    extern int ga, gb;                                                          \
    void name(int a, int b) { ga = a; gb = b; }
SET2(Z_5FDB38, g_6543a8, g_654398)
SET2(Z_628CE6, g_64c2c0, g_64c2c4)

// ---- 108: compare with a global id (same global in both copies)
extern int g_63afe8;
bool Z_42DCA9(int id) { return id == g_63afe8; }
bool Z_611B31(int id) { return id == g_63afe8; }

// ---- 111: toggle a global flag
extern bool g_6390a8, g_639357;
void Z_600603() { g_6390a8 = !g_6390a8; }
void Z_618C8C() { g_639357 = !g_639357; }

// ---- 112/113: forward to slot 11 of an embedded object
struct ZTSlot11 { virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
                  virtual void s5(); virtual void s6(); virtual void s7(); virtual void s8(); virtual void s9();
                  virtual void s10(); virtual void run(); };
#define FWD_EMBEDDED(cls, off)                                                  \
    struct cls { BYTE m_unk00[off]; ZTSlot11 m_sub; void f(); };                \
    void cls::f() { m_sub.run(); }
FWD_EMBEDDED(Z_4D954A, 0x1e0)
FWD_EMBEDDED(Z_4DBF90, 0x1e0)
FWD_EMBEDDED(Z_4D9573, 0x1e8)
FWD_EMBEDDED(Z_5ACF8A, 0x1e8)

// ---- 114: drop a use count
struct ZTCounted { BYTE m_unk00[0x20]; int m_uses; };
void Z_422B05(ZTCounted** pp) { if (*pp) --(*pp)->m_uses; }
void Z_4A0655(ZTCounted** pp) { if (*pp) --(*pp)->m_uses; }

// ---- 110: forward with a constant
#define FWD_1(name, callee)                                                     \
    void callee(int a, int b);                                                  \
    void name(int a) { callee(a, 1); }
FWD_1(Z_46AB65, f46aa89)
FWD_1(Z_512C87, f512970)

// ---- 104 / 93 / 88: member forwards that keep `this` in ecx for the callee (thiscall, ecx untouched)
#define FWD2_1(cls, callee)                                                     \
    struct cls { bool callee(int a, int b, int c); bool f(int a, int b); };     \
    bool cls::f(int a, int b) { return callee(a, b, 1); }
FWD2_1(Z_49A147, m499886)
FWD2_1(Z_4A75A7, m425533)

struct Z_4435B9 { void m4435a8(int a, int b, int c); int f(int a, int b, int c); };
int Z_4435B9::f(int a, int b, int c) { m4435a8(a, b, c); return 0; }
struct Z_620299 : Z_4435B9 { int f(int a, int b, int c); };
int Z_620299::f(int a, int b, int c) { Z_4435B9::f(a, b, c); return 0; }

#define FWD4(cls, callee)                                                       \
    struct cls { int callee(int a, int b, int c, int d); int f(int a, int b, int c, int d); }; \
    int cls::f(int a, int b, int c, int d) { return callee(a, b, c, d); }
FWD4(Z_612EDB, m602307)
FWD4(Z_61B61D, m610f8f)

// ---- 100: call through member +0x128 with a dereferenced argument
#define FWD_128(cls, tcls, method)                                              \
    struct tcls { void method(int v); };                                        \
    struct cls { BYTE m_unk00[0x128]; tcls* m_unk128; void f(int* p); };        \
    void cls::f(int* p) { m_unk128->method(*p); }
FWD_128(Z_410FFE, ZTT402062, m402062)
FWD_128(Z_4408B4, ZTT44084B, m44084b)

// ---- 101 / 91 / 84: calls with the shared descriptor g_639360
extern char g_639360;
#define FWD_8(cls, tcls, method)                                                \
    struct tcls { void method(int a, void* d); };                               \
    struct cls { BYTE m_unk00[8]; tcls* m_unk08; void f(int a); };              \
    void cls::f(int a) { m_unk08->method(a, &g_639360); }
FWD_8(Z_4708EA, ZTT41308D, m41308d)
FWD_8(Z_603FDD, ZTT41303C, m41303c)

#define RESET_2(cls, m1, m2)                                                    \
    struct cls { void m1(int a, void* d); void m2(int a); void f(); };          \
    void cls::f() { m1(0, &g_639360); m2(0); }
RESET_2(Z_4131F9, m41308d, m4131c8)
RESET_2(Z_43E8F4, m41303c, m41300b)

struct ZTT41322B { void m41322b(int a, int b, int c, void* d, int e); };
#define FWD_15C(cls)                                                            \
    struct cls { BYTE m_unk00[0x15c]; ZTT41322B m_sub; void f(int a, int b); }; \
    void cls::f(int a, int b) { m_sub.m41322b(a, b, 0, &g_639360, 0); }
FWD_15C(Z_43E8D3)
FWD_15C(Z_6022C8)

// ---- 102: tell the main screen to refresh
struct ZTScreen4B2322 { void m4b2322(int a, int b); };
class UIControl;
UIControl* UIH_4017E5();
void Z_4B2355() { ZTScreen4B2322* s = (ZTScreen4B2322*)UIH_4017E5(); if (s) s->m4b2322(0, 1); }
void Z_4ED80A() { ZTScreen4B2322* s = (ZTScreen4B2322*)UIH_4017E5(); if (s) s->m4b2322(0, 1); }

// ---- 98: store a flag and notify
#define FLAG_13F(cls, notify)                                                   \
    struct cls { BYTE m_unk00[0x13f]; char m_unk13F; void f(char a); };          \
    void notify(cls* o, char a);                                                \
    void cls::f(char a) { m_unk13F = a; notify(this, a); }
FLAG_13F(Z_42AA0A, f42a9fa)
FLAG_13F(Z_43F0D5, f43f0c5)

// ---- 96: reset and run slot 7
struct ZTFlag10 { BYTE m_unk00[0x10]; bool m_unk10; };
#define RESET_RUN(cls)                                                          \
    struct cls {                                                                \
        virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); \
        virtual void s4(); virtual void s5(); virtual void s6(); virtual void run(); \
        BYTE m_unk04[0x18 - 4]; int m_unk18; BYTE m_unk1C[0x4d - 0x1c]; bool m_unk4D; \
        BYTE m_unk4E[0x54 - 0x4e]; ZTFlag10* m_unk54; void f(); };              \
    void cls::f() { m_unk18 = 0; if (m_unk54) m_unk54->m_unk10 = true; m_unk4D = false; run(); }
RESET_RUN(Z_413304)
RESET_RUN(Z_43EACC)

// ---- 89: arm and run slot 16
#define ARM_RUN(cls)                                                            \
    struct cls {                                                                \
        virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); \
        virtual void s4(); virtual void s5(); virtual void s6(); virtual void s7(); \
        virtual void s8(); virtual void s9(); virtual void s10(); virtual void s11(); \
        virtual void s12(); virtual void s13(); virtual void s14(); virtual void s15(); \
        virtual void run();                                                     \
        BYTE m_unk04[0x4a4 - 4]; bool m_unk4A4; BYTE m_unk4A5[0x508 - 0x4a5]; bool m_unk508; \
        void f(); };                                                            \
    void cls::f() { if (m_unk4A4) { m_unk508 = true; run(); } }
ARM_RUN(Z_4D5DFE)
ARM_RUN(Z_4D6F6B)

// ---- 94: forward with a computed second argument
#define FWD_COMPUTED(cls, getter)                                               \
    struct cls { int getter(); void m49e9c2(int a, int b); void f(int a); };    \
    void cls::f(int a) { m49e9c2(a, getter()); }
FWD_COMPUTED(Z_49EBCE, m411285)
FWD_COMPUTED(Z_4A8A23, m410349)

// ---- 80: store a 12-byte value, then update the member object at +0x1BC
struct ZTVec3 { int x, y, z; };
#define SET_POS(cls, tcls, method)                                              \
    struct tcls { void method(); };                                             \
    struct cls { BYTE m_unk00[0x1bc]; tcls m_sub; BYTE m_unk1BD[0x1dc - 0x1bd]; ZTVec3 m_pos; \
                 void f(const ZTVec3& v); };                                    \
    void cls::f(const ZTVec3& v) { m_pos = v; m_sub.method(); }
SET_POS(Z_43D25E, ZTT43D286, m43d286)
SET_POS(Z_48BF55, ZTT48BF7D, m48bf7d)

// ---- 79: factory (operator new 0x402A5A, out-of-line ctor)
#define CREATE2(name, cls)                                                      \
    struct cls { cls(int a, int b); BYTE m_data[0x14]; };                       \
    cls* __stdcall name(int a, int b) { return new cls(a, b); }
CREATE2(Z_413AA7, ZTObj413A87)
CREATE2(Z_413BEC, ZTObj413BA8)

// ---- 67: return a 12-byte value produced by the member at +8
#define GET_VEC(cls, tcls, method)                                              \
    struct tcls { ZTVec3 method(); };                                           \
    struct cls { BYTE m_unk00[8]; tcls* m_unk08; ZTVec3 f(); };                 \
    ZTVec3 cls::f() { return m_unk08->method(); }
GET_VEC(Z_603FF2, ZTT603433, m603433)
GET_VEC(Z_604021, ZTT4971A9, m4971a9)
GET_VEC(Z_604070, ZTT4993D7, m4993d7)
```
