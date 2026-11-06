# Removed: Src/misc/fwd11a4.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: one-letter method names: f, g
- formatting: 6 packed + 0 overlong lines of 33
- readability: macro-stamped function family FWD_11A4

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (6)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x485dd5 | `?f@Z_485DD5@@QAEXXZ` | matched (zoo.map) |
| 0x4c9d67 | `?f@Z_4C9D67@@QAEXXZ` | matched (zoo.map) |
| 0x4ca2fb | `?f@Z_4CA2FB@@QAEXXZ` | matched (zoo.map) |
| 0x4ca478 | `?f@Z_4CA478@@QAEXXZ` | matched (zoo.map) |
| 0x4cc59d | `?f@Z_4CC59D@@QAEXXZ` | matched (zoo.map) |
| 0x592562 | `?f@Z_592562@@QAEXXZ` | matched (zoo.map) |

## Matching source per function

### 0x485dd5 `?f@Z_485DD5@@QAEXXZ`

```cpp
FWD_11A4(Z_485DD5)
```

### 0x4c9d67 `?f@Z_4C9D67@@QAEXXZ`

```cpp
FWD_11A4(Z_4C9D67)
```

### 0x4ca2fb `?f@Z_4CA2FB@@QAEXXZ`

```cpp
FWD_11A4(Z_4CA2FB)
```

### 0x4ca478 `?f@Z_4CA478@@QAEXXZ`

```cpp
FWD_11A4(Z_4CA478)
```

### 0x4cc59d `?f@Z_4CC59D@@QAEXXZ`

```cpp
FWD_11A4(Z_4CC59D)
```

### 0x592562 `?f@Z_592562@@QAEXXZ`

```cpp
FWD_11A4(Z_592562)
```

## Full original file (reference only, not compiled)

```cpp
// fwd11a4.cpp - six copies of `if (m_11a4) m_11a4->g();` (one per class; names Z_<address>), with the
// callee g (0x592570) that BBT placed behind the last copy (0x592562).
struct G592570
{
    struct Target { virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
                    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
                    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
                    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
                    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
                    virtual bool v20(); };                                  // slot 20 (+0x50)
    Target* m_target;                                 // +0
    bool m_done;                                      // +4
    int m_unk8;                                       // +8
    void g();
};
void G592570::g()
{
    if (!m_done && m_target && m_target->v20()) {
        m_done = true;
        m_unk8 = 0;
    }
}
#define FWD_11A4(name)                                                          \
    struct name { unsigned char m_unk00[0x11a4]; G592570* m_11a4; void f(); };  \
    void name::f()                                                              \
    {                                                                           \
        if (m_11a4)                                                             \
            m_11a4->g();                                                        \
    }
FWD_11A4(Z_485DD5)
FWD_11A4(Z_4C9D67)
FWD_11A4(Z_4CA2FB)
FWD_11A4(Z_4CA478)
FWD_11A4(Z_4CC59D)
FWD_11A4(Z_592562)
```
