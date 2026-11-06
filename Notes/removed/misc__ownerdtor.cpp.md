# Removed: Src/misc/ownerdtor.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 2, e.g. Z_40D8EC, Z_635830

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// ownerdtor.cpp - destructor of a small owner class (vtable 0x630C24, base vtable 0x635830) that is
// emitted in six translation units (header-inline): release() deletes the owned object.
// Notes/instances_ownerdtor.csv maps the six copies to Z_40D8EC::~Z_40D8EC.
struct Z_635830
{
    virtual ~Z_635830();                              // 0x40D920 (out of line: only resets the vptr)
};
Z_635830::~Z_635830()
{
}
struct Z_Owned { virtual ~Z_Owned(); };
struct Z_40D8EC : Z_635830
{
    Z_Owned* m_owned;                                 // +4
    void release();                                   // out of line; BBT inlines it into the dtor
    virtual ~Z_40D8EC();
};
void Z_40D8EC::release()
{
    if (m_owned) {
        delete m_owned;
        m_owned = 0;
    }
}
Z_40D8EC::~Z_40D8EC()
{
    release();
}
```
