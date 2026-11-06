# Removed: Src/misc/strtemp.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 3, e.g. Z_4BAE0A, Z_5FFF85, Z_61517E
- descriptive names: one-letter method names: f

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (3)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x4bae0a | `?f@Z_4BAE0A@@QAE_NXZ` | matched (zoo.map) |
| 0x5fff85 | `?f@Z_5FFF85@@QAE_NXZ` | matched (zoo.map) |
| 0x61517e | `?f@Z_61517E@@QAE_NXZ` | matched (zoo.map) |

## Matching source per function

### 0x4bae0a `?f@Z_4BAE0A@@QAE_NXZ`

```cpp
struct Z_4BAE0A
{
    bool m4b4622(_STL::string& out);
    bool f();
};

bool Z_4BAE0A::f()
{
    _STL::string s;
    return m4b4622(s);
}
```

### 0x5fff85 `?f@Z_5FFF85@@QAE_NXZ`

```cpp
struct Z_5FFF85 : Z_4BAE0A { bool f(); };

bool Z_5FFF85::f() { return Z_4BAE0A::f(); }
```

### 0x61517e `?f@Z_61517E@@QAE_NXZ`

```cpp
struct Z_61517E : Z_4BAE0A { bool f(); };

bool Z_61517E::f() { return Z_4BAE0A::f(); }
```

## Full original file (reference only, not compiled)

```cpp
// strtemp.cpp - members that fill a local string through another member and return its bool result
// (cluster 0x4bae0a; 0x5fff85 / 0x61517e are one-jmp wrappers of it). Names are placeholders Z_<address>.
#include <string>

struct Z_4BAE0A
{
    bool m4b4622(_STL::string& out);
    bool f();
};
bool Z_4BAE0A::f()
{
    _STL::string s;
    return m4b4622(s);
}

struct Z_5FFF85 : Z_4BAE0A { bool f(); };
bool Z_5FFF85::f() { return Z_4BAE0A::f(); }
struct Z_61517E : Z_4BAE0A { bool f(); };
bool Z_61517E::f() { return Z_4BAE0A::f(); }
```
