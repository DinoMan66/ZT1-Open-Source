# Removed: Src/reg/stl_inst8.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- formatting: 21 packed + 0 overlong lines of 41

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Full original file (reference only, not compiled)

```cpp
// stl_inst8.cpp - std::string members and more tree/list shapes, instantiated by use
// (Tools/shapescan.py -> Notes/instances_stl8.csv). Keep unchanged once listed.
#include <string>
#include <map>
#include <set>
#include <list>
#include <vector>
#include <algorithm>

typedef std::string S;
void use8(S& a, const S& b, const char* c, char ch, int n)
{
    a.append(b); a.append(c); a.append(c, n); a.append(n, ch); a += b; a += c; a += ch;
    a.assign(b); a.assign(c); a.assign(c, n); a.assign(n, ch);
    a.insert(0, b); a.insert(0, c); a.insert(a.begin(), ch); a.insert((size_t)0, (size_t)n, ch);
    a.erase(0, 1); a.erase(a.begin()); a.erase(a.begin(), a.end());
    a.replace(0, 1, b); a.replace(0, 1, c); a.replace(0, 1, n, ch);
    a.find(b); a.find(c); a.find(ch); a.rfind(b); a.rfind(c); a.rfind(ch);
    a.find_first_of(b); a.find_first_of(c); a.find_last_of(c); a.find_first_not_of(c); a.find_last_not_of(c);
    a.substr(1, 2); a.compare(b); a.compare(c); a.compare(0, 1, b);
    a.resize(5); a.resize(6, ch); a.reserve(20); a.swap(const_cast<S&>(b));
    S d = a + b; S e = a + c; S f = c + a; S g = a + ch; S h(b, 1, 2); S i(n, ch); S j(c, n);
    bool r = (a == b) || (a == c) || (a < b) || (a != c) || (c == a);
    a.copy(const_cast<char*>(c), 1, 0);
    std::sort(a.begin(), a.end());
}
void use8b(std::map<S, float>& a, std::map<S, std::pair<int,int> >& b, std::map<S, std::list<int> >& c,
           std::set<unsigned short>& d, std::map<unsigned short, int>& e, std::map<int, float>& f,
           std::list<std::pair<S, int> >& g, std::vector<std::pair<S, int> >& h, std::multimap<S, int>& i,
           std::multiset<int>& j, std::map<char, int>& k, std::map<S, S*>& l)
{
    a[S("x")] = 1.0f; a.erase(S("x")); a.find(S("y")); a.clear();
    b[S("x")].first = 1; b.erase(S("x")); b.find(S("y")); b.clear();
    c[S("x")].push_back(1); c.erase(S("x")); c.clear();
    d.insert(1); d.erase(1); d.find(2); d.clear();
    e[1] = 2; e.erase(1); e.find(2); e.clear();
    f[1] = 2.0f; f.erase(1); f.find(2); f.clear();
    g.push_back(std::make_pair(S("x"), 1)); g.clear();
    h.push_back(std::make_pair(S("x"), 1)); h.erase(h.begin()); h.clear();
    i.insert(std::make_pair(S("x"), 1)); i.erase(S("x")); i.find(S("x")); i.clear();
    j.insert(1); j.erase(1); j.find(1); j.clear();
    k['a'] = 1; k.erase('a'); k.find('b'); k.clear();
    l[S("x")] = 0; l.erase(S("x")); l.find(S("y")); l.clear();
}
```
