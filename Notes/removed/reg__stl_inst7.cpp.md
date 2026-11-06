# Removed: Src/reg/stl_inst7.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- formatting: 64 packed + 0 overlong lines of 147

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_inst7.cpp - STLport members for POD element types of several sizes (vector/list/deque/map),
// instantiated by use; Tools/shapescan.py -> Notes/instances_stl7.csv. Keep unchanged once listed.
#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <algorithm>
#include <string>

struct P8 { int a[2]; };
inline bool operator<(const P8& x, const P8& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P8& x, const P8& y) { return x.a[0] == y.a[0]; }
struct P12 { int a[3]; };
inline bool operator<(const P12& x, const P12& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P12& x, const P12& y) { return x.a[0] == y.a[0]; }
struct P16 { int a[4]; };
inline bool operator<(const P16& x, const P16& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P16& x, const P16& y) { return x.a[0] == y.a[0]; }
struct P20 { int a[5]; };
inline bool operator<(const P20& x, const P20& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P20& x, const P20& y) { return x.a[0] == y.a[0]; }
struct P24 { int a[6]; };
inline bool operator<(const P24& x, const P24& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P24& x, const P24& y) { return x.a[0] == y.a[0]; }
struct P28 { int a[7]; };
inline bool operator<(const P28& x, const P28& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P28& x, const P28& y) { return x.a[0] == y.a[0]; }
struct P32 { int a[8]; };
inline bool operator<(const P32& x, const P32& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P32& x, const P32& y) { return x.a[0] == y.a[0]; }
struct P36 { int a[9]; };
inline bool operator<(const P36& x, const P36& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P36& x, const P36& y) { return x.a[0] == y.a[0]; }
struct P40 { int a[10]; };
inline bool operator<(const P40& x, const P40& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P40& x, const P40& y) { return x.a[0] == y.a[0]; }
struct P44 { int a[11]; };
inline bool operator<(const P44& x, const P44& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P44& x, const P44& y) { return x.a[0] == y.a[0]; }
struct P48 { int a[12]; };
inline bool operator<(const P48& x, const P48& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P48& x, const P48& y) { return x.a[0] == y.a[0]; }
struct P64 { int a[16]; };
inline bool operator<(const P64& x, const P64& y) { return x.a[0] < y.a[0]; }
inline bool operator==(const P64& x, const P64& y) { return x.a[0] == y.a[0]; }

void use7_8(std::vector<P8>& v, std::list<P8>& l, std::map<int, P8>& m, std::deque<P8>& d, const P8& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P8> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_12(std::vector<P12>& v, std::list<P12>& l, std::map<int, P12>& m, std::deque<P12>& d, const P12& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P12> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_16(std::vector<P16>& v, std::list<P16>& l, std::map<int, P16>& m, std::deque<P16>& d, const P16& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P16> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_20(std::vector<P20>& v, std::list<P20>& l, std::map<int, P20>& m, std::deque<P20>& d, const P20& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P20> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_24(std::vector<P24>& v, std::list<P24>& l, std::map<int, P24>& m, std::deque<P24>& d, const P24& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P24> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_28(std::vector<P28>& v, std::list<P28>& l, std::map<int, P28>& m, std::deque<P28>& d, const P28& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P28> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_32(std::vector<P32>& v, std::list<P32>& l, std::map<int, P32>& m, std::deque<P32>& d, const P32& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P32> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_36(std::vector<P36>& v, std::list<P36>& l, std::map<int, P36>& m, std::deque<P36>& d, const P36& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P36> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_40(std::vector<P40>& v, std::list<P40>& l, std::map<int, P40>& m, std::deque<P40>& d, const P40& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P40> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_44(std::vector<P44>& v, std::list<P44>& l, std::map<int, P44>& m, std::deque<P44>& d, const P44& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P44> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_48(std::vector<P48>& v, std::list<P48>& l, std::map<int, P48>& m, std::deque<P48>& d, const P48& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P48> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_64(std::vector<P64>& v, std::list<P64>& l, std::map<int, P64>& m, std::deque<P64>& d, const P64& x)
{
    v.push_back(x); v.insert(v.begin(), x); v.insert(v.end(), 3, x); v.erase(v.begin()); v.resize(5); v.reserve(10);
    std::vector<P64> w(v); w = v; v.swap(w); v.erase(v.begin(), v.end());
    l.push_back(x); l.push_front(x); l.insert(l.begin(), x); l.erase(l.begin()); l.remove(x); l.sort(); l.clear();
    m[1] = x; m.insert(std::make_pair(2, x)); m.erase(1); m.find(2); m.clear();
    d.push_back(x); d.push_front(x); d.pop_back(); d.pop_front(); d.clear();
}
void use7_misc(std::vector<int>& v, std::vector<void*>& p, std::vector<float>& f, std::vector<std::string>& s)
{
    std::sort(v.begin(), v.end()); std::find(v.begin(), v.end(), 3); v.insert(v.begin(), 4, 1); v.resize(9, 2);
    p.insert(p.begin(), (void*)0); std::find(p.begin(), p.end(), (void*)0); p.erase(p.begin(), p.end());
    f.push_back(1.0f); f.insert(f.begin(), 2.0f); f.resize(4);
    s.insert(s.begin(), std::string("a")); s.resize(3); std::sort(s.begin(), s.end());
    std::vector<int> w(v); v = w;
}
```
