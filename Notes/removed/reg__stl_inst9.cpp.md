# Removed: Src/reg/stl_inst9.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- formatting: 34 packed + 0 overlong lines of 95

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_inst9.cpp - string-keyed maps and sets of POD values of several sizes (see stl_inst7.cpp),
// Tools/shapescan.py -> Notes/instances_stl9.csv. Keep unchanged once listed.
#include <vector>
#include <list>
#include <map>
#include <set>
#include <string>

struct Q8 { int a[2]; };
inline bool operator<(const Q8& x, const Q8& y) { return x.a[0] < y.a[0]; }
struct Q12 { int a[3]; };
inline bool operator<(const Q12& x, const Q12& y) { return x.a[0] < y.a[0]; }
struct Q16 { int a[4]; };
inline bool operator<(const Q16& x, const Q16& y) { return x.a[0] < y.a[0]; }
struct Q20 { int a[5]; };
inline bool operator<(const Q20& x, const Q20& y) { return x.a[0] < y.a[0]; }
struct Q24 { int a[6]; };
inline bool operator<(const Q24& x, const Q24& y) { return x.a[0] < y.a[0]; }
struct Q28 { int a[7]; };
inline bool operator<(const Q28& x, const Q28& y) { return x.a[0] < y.a[0]; }
struct Q32 { int a[8]; };
inline bool operator<(const Q32& x, const Q32& y) { return x.a[0] < y.a[0]; }
struct Q36 { int a[9]; };
inline bool operator<(const Q36& x, const Q36& y) { return x.a[0] < y.a[0]; }
struct Q40 { int a[10]; };
inline bool operator<(const Q40& x, const Q40& y) { return x.a[0] < y.a[0]; }
struct Q48 { int a[12]; };
inline bool operator<(const Q48& x, const Q48& y) { return x.a[0] < y.a[0]; }
struct Q64 { int a[16]; };
inline bool operator<(const Q64& x, const Q64& y) { return x.a[0] < y.a[0]; }
void use9_8(std::map<std::string, Q8>& m, std::set<Q8>& s, std::map<unsigned, Q8>& u, std::vector<Q8*>& p, const Q8& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_12(std::map<std::string, Q12>& m, std::set<Q12>& s, std::map<unsigned, Q12>& u, std::vector<Q12*>& p, const Q12& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_16(std::map<std::string, Q16>& m, std::set<Q16>& s, std::map<unsigned, Q16>& u, std::vector<Q16*>& p, const Q16& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_20(std::map<std::string, Q20>& m, std::set<Q20>& s, std::map<unsigned, Q20>& u, std::vector<Q20*>& p, const Q20& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_24(std::map<std::string, Q24>& m, std::set<Q24>& s, std::map<unsigned, Q24>& u, std::vector<Q24*>& p, const Q24& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_28(std::map<std::string, Q28>& m, std::set<Q28>& s, std::map<unsigned, Q28>& u, std::vector<Q28*>& p, const Q28& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_32(std::map<std::string, Q32>& m, std::set<Q32>& s, std::map<unsigned, Q32>& u, std::vector<Q32*>& p, const Q32& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_36(std::map<std::string, Q36>& m, std::set<Q36>& s, std::map<unsigned, Q36>& u, std::vector<Q36*>& p, const Q36& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_40(std::map<std::string, Q40>& m, std::set<Q40>& s, std::map<unsigned, Q40>& u, std::vector<Q40*>& p, const Q40& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_48(std::map<std::string, Q48>& m, std::set<Q48>& s, std::map<unsigned, Q48>& u, std::vector<Q48*>& p, const Q48& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_64(std::map<std::string, Q64>& m, std::set<Q64>& s, std::map<unsigned, Q64>& u, std::vector<Q64*>& p, const Q64& x)
{
    m[std::string("a")] = x; m.erase(std::string("a")); m.find(std::string("b")); m.clear();
    s.insert(x); s.erase(x); s.find(x); s.clear();
    u[1u] = x; u.erase(1u); u.find(2u); u.clear();
}
void use9_more(std::map<int, std::string*>& a, std::map<int, std::list<std::string> >& b, std::list<std::list<int> >& c)
{ a[1] = 0; a.erase(1); b[1].push_back(std::string("x")); b.erase(1); c.push_back(std::list<int>()); c.clear(); }
```
