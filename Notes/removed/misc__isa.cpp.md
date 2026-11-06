# Removed: Src/misc/isa.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 1, e.g. Z_402232
- readability: macro-stamped function family ISA

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (20)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x40175b | `?isA@Z_40175B@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x402232 | `?isA@Z_402232@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x402260 | `?isA@Z_402260@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4022a4 | `?isA@Z_4022A4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4022e2 | `?isA@Z_4022E2@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa361 | `?isA@Z_4AA361@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa3ff | `?isA@Z_4AA3FF@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa43a | `?isA@Z_4AA43A@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa47b | `?isA@Z_4AA47B@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa4bc | `?isA@Z_4AA4BC@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa570 | `?isA@Z_4AA570@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa5ae | `?isA@Z_4AA5AE@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa6b4 | `?isA@Z_4AA6B4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa6f2 | `?isA@Z_4AA6F2@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa730 | `?isA@Z_4AA730@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa774 | `?isA@Z_4AA774@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa7e4 | `?isA@Z_4AA7E4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa825 | `?isA@Z_4AA825@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa866 | `?isA@Z_4AA866@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa8a4 | `?isA@Z_4AA8A4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |

## Matching source per function

### 0x40175b `?isA@Z_40175B@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_40175B, Z_4022A4, g_638700)
```

### 0x402232 `?isA@Z_402232@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
struct Z_402232 {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C();
    virtual void v10();
    virtual const String& type() const;                     // slot 0x14
    bool isA(const String& s);
};

bool Z_402232::isA(const String& s)
{
    return type() == s;
}
```

### 0x402260 `?isA@Z_402260@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_402260, Z_4022A4, g_638690)
```

### 0x4022a4 `?isA@Z_4022A4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4022A4, Z_4022E2, g_6386b0)
```

### 0x4022e2 `?isA@Z_4022E2@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4022E2, Z_402232, g_6386b0)
```

### 0x4aa361 `?isA@Z_4AA361@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA361, Z_4AA3FF, g_6386c0)
```

### 0x4aa3ff `?isA@Z_4AA3FF@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA3FF, Z_402232, g_638670)
```

### 0x4aa43a `?isA@Z_4AA43A@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA43A, Z_4AA3FF, g_6386a0)
```

### 0x4aa47b `?isA@Z_4AA47B@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA47B, Z_4AA3FF, g_638660)
```

### 0x4aa4bc `?isA@Z_4AA4BC@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA4BC, Z_4AA3FF, g_638680)
```

### 0x4aa570 `?isA@Z_4AA570@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA570, Z_4AA5AE, g_638780)
```

### 0x4aa5ae `?isA@Z_4AA5AE@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA5AE, Z_4022A4, g_638710)
```

### 0x4aa6b4 `?isA@Z_4AA6B4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA6B4, Z_4AA5AE, g_638760)
```

### 0x4aa6f2 `?isA@Z_4AA6F2@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA6F2, Z_4AA5AE, g_638770)
```

### 0x4aa730 `?isA@Z_4AA730@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA730, Z_4AA774, g_638740)
```

### 0x4aa774 `?isA@Z_4AA774@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA774, Z_402232, g_638750)
```

### 0x4aa7e4 `?isA@Z_4AA7E4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA7E4, Z_4AA47B, g_638720)
```

### 0x4aa825 `?isA@Z_4AA825@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA825, Z_4AA3FF, g_6387a0)
```

### 0x4aa866 `?isA@Z_4AA866@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA866, Z_4AA5AE, g_638790)
```

### 0x4aa8a4 `?isA@Z_4AA8A4@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
ISA(Z_4AA8A4, Z_4AA3FF, g_639100)
```

## Full original file (reference only, not compiled)

```cpp
// isa.cpp - run-time type test chain: every class answers isA(name) with its own type-name string or
// asks its base; the root compares the virtual type() result. Names are placeholders Z_<address>.
// BBT inlined the root into the first level (sub esp,4 frames), so the root has to live in this object.
#include <string>

typedef _STL::string String;

struct Z_402232 {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C();
    virtual void v10();
    virtual const String& type() const;                     // slot 0x14
    bool isA(const String& s);
};
bool Z_402232::isA(const String& s)
{
    return type() == s;
}

#define ISA(cls, base, str)                                                     \
    extern const String str;                                                    \
    struct cls : base { bool isA(const String& s); };                           \
    bool cls::isA(const String& s)                                              \
    {                                                                           \
        return s == str || base::isA(s);                                        \
    }

ISA(Z_4022E2, Z_402232, g_6386b0)
ISA(Z_4022A4, Z_4022E2, g_6386b0)
ISA(Z_40175B, Z_4022A4, g_638700)
ISA(Z_402260, Z_4022A4, g_638690)
ISA(Z_4AA5AE, Z_4022A4, g_638710)
ISA(Z_4AA570, Z_4AA5AE, g_638780)
ISA(Z_4AA6B4, Z_4AA5AE, g_638760)
ISA(Z_4AA6F2, Z_4AA5AE, g_638770)
ISA(Z_4AA866, Z_4AA5AE, g_638790)
ISA(Z_4AA3FF, Z_402232, g_638670)
ISA(Z_4AA361, Z_4AA3FF, g_6386c0)
ISA(Z_4AA43A, Z_4AA3FF, g_6386a0)
ISA(Z_4AA4BC, Z_4AA3FF, g_638680)
ISA(Z_4AA825, Z_4AA3FF, g_6387a0)
ISA(Z_4AA47B, Z_4AA3FF, g_638660)
ISA(Z_4AA7E4, Z_4AA47B, g_638720)
ISA(Z_4AA774, Z_402232, g_638750)
ISA(Z_4AA730, Z_4AA774, g_638740)
ISA(Z_4AA8A4, Z_4AA3FF, g_639100)
```
