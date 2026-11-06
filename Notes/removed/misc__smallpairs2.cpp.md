# Removed: Src/misc/smallpairs2.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 2, e.g. Z_5B241E, Z_5B24AE
- descriptive names: one-letter method names: f
- formatting: 16 packed + 1 overlong lines of 96

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (4)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x4a9b8e | `?f@Z_4A9B8E@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x4aa02f | `?f@Z_4AA02F@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z` | matched (zoo.map) |
| 0x5b241e | `?f@Z_5B241E@@QAEXXZ` | matched (zoo.map) |
| 0x5b24ae | `?f@Z_5B24AE@@QAEXXZ` | matched (zoo.map) |

## Matching source per function

### 0x4a9b8e `?f@Z_4A9B8E@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
NAME_IS(Z_4A9B8E, g_6393a4)
```

### 0x4aa02f `?f@Z_4AA02F@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@_STL@@@_STL@@@Z`

```cpp
NAME_IS(Z_4AA02F, g_63943c)
```

### 0x5b241e `?f@Z_5B241E@@QAEXXZ`

```cpp
struct Z_5B241E
{
    BYTE m_unk00[0x154];
    _STL::list<ZTRec16> m_recs;                              // +0x154
    BYTE m_unk158[4];
    ZTSlot8 m_sub;                                           // +0x15C
    void f();
};

void Z_5B241E::f()
{
    m_recs.clear();
    m_sub.run();
}
```

### 0x5b24ae `?f@Z_5B24AE@@QAEXXZ`

```cpp
struct Z_5B24AE : Z_5B241E { void f(); };

void Z_5B24AE::f() { Z_5B241E::f(); }
```

## Full original file (reference only, not compiled)

```cpp
// smallpairs2.cpp - more functions that occur twice with the same code (Notes/generated/clusters.md 71-76).
// Names are placeholders Z_<address>.
#include <string>
#include <vector>
#include <list>
typedef unsigned char BYTE;

struct ZTKind2 { virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
                 virtual void s5(); virtual void s6(); virtual bool isKindOf(const void* type); };

// ---- 71: send <arg> to every object of the game's list whose id (slot 8) is <id>
struct ZTListed {
    virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
    virtual void s5(); virtual void s6(); virtual void s7();
    virtual int  id();                                       // slot 8
    virtual void s9(); virtual void s10(); virtual void s11(); virtual void s12(); virtual void s13();
    virtual void s14();
    virtual void notify(int arg);                            // slot 15
};
struct ZTGame98 { BYTE m_unk00[0x98]; _STL::vector<ZTListed*> m_objects; };
extern ZTGame98* g_638040;
#define NOTIFY_ID(name)                                                         \
    void name(int id, int arg)                                                  \
    {                                                                           \
        _STL::vector<ZTListed*>& v = g_638040->m_objects;                       \
        for (ZTListed** it = v.begin(); it != v.end(); ++it) {                  \
            ZTListed* o = *it;                                                  \
            if (o && o->id() == id)                                             \
                o->notify(arg);                                                 \
        }                                                                       \
    }
NOTIFY_ID(Z_58FD9F)
NOTIFY_ID(Z_591325)

// ---- 74: when enabled, update every listed item whose slot 8 says so
struct ZTItem74 {
    virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
    virtual void s5(); virtual void s6(); virtual void s7();
    virtual bool dirty();                                    // slot 8
    void m505099();
    void m6066eb();
};
struct ZTList74 { BYTE m_unk00[0x1c]; _STL::vector<ZTItem74*> m_items; };
extern ZTList74* g_63805c;
#define UPDATE_DIRTY(cls, method)                                               \
    struct cls { BYTE m_unk00[0x1f0]; bool m_unk1F0; void f(); };               \
    void cls::f()                                                               \
    {                                                                           \
        if (!m_unk1F0)                                                          \
            return;                                                             \
        _STL::vector<ZTItem74*>& v = g_63805c->m_items;                         \
        for (ZTItem74** it = v.begin(); it != v.end(); ++it) {                  \
            ZTItem74* o = *it;                                                  \
            if (o->dirty())                                                     \
                o->method();                                                    \
        }                                                                       \
    }
UPDATE_DIRTY(Z_479EBA, m505099)
UPDATE_DIRTY(Z_47A162, m6066eb)

// ---- 75: clear the list at +0x154, then run slot 8 of the object at +0x15C (0x5B24AE is a jmp to it)
struct ZTRec16 { int a, b, c, d; };
struct ZTSlot8 { virtual void s0(); virtual void s1(); virtual void s2(); virtual void s3(); virtual void s4();
                 virtual void s5(); virtual void s6(); virtual void s7(); virtual void run(); };
struct Z_5B241E
{
    BYTE m_unk00[0x154];
    _STL::list<ZTRec16> m_recs;                              // +0x154
    BYTE m_unk158[4];
    ZTSlot8 m_sub;                                           // +0x15C
    void f();
};
void Z_5B241E::f()
{
    m_recs.clear();
    m_sub.run();
}
struct Z_5B24AE : Z_5B241E { void f(); };
void Z_5B24AE::f() { Z_5B241E::f(); }

// ---- 73: pass the owner's value +0x1EC to the helper object (slot 147) if the owner is a <g_638690>
struct ZTHelper73 { int m4388d7(int v, int a); int m43c376(int v, int a); };
struct ZTOwner73 : ZTKind2 { BYTE m_unk04[0x1ec - 4]; int m_unk1EC; };
struct ZTV147 { virtual void v000(); virtual void v001(); virtual void v002(); virtual void v003(); virtual void v004(); virtual void v005(); virtual void v006(); virtual void v007(); virtual void v008(); virtual void v009(); virtual void v010(); virtual void v011(); virtual void v012(); virtual void v013(); virtual void v014(); virtual void v015(); virtual void v016(); virtual void v017(); virtual void v018(); virtual void v019(); virtual void v020(); virtual void v021(); virtual void v022(); virtual void v023(); virtual void v024(); virtual void v025(); virtual void v026(); virtual void v027(); virtual void v028(); virtual void v029(); virtual void v030(); virtual void v031(); virtual void v032(); virtual void v033(); virtual void v034(); virtual void v035(); virtual void v036(); virtual void v037(); virtual void v038(); virtual void v039(); virtual void v040(); virtual void v041(); virtual void v042(); virtual void v043(); virtual void v044(); virtual void v045(); virtual void v046(); virtual void v047(); virtual void v048(); virtual void v049(); virtual void v050(); virtual void v051(); virtual void v052(); virtual void v053(); virtual void v054(); virtual void v055(); virtual void v056(); virtual void v057(); virtual void v058(); virtual void v059(); virtual void v060(); virtual void v061(); virtual void v062(); virtual void v063(); virtual void v064(); virtual void v065(); virtual void v066(); virtual void v067(); virtual void v068(); virtual void v069(); virtual void v070(); virtual void v071(); virtual void v072(); virtual void v073(); virtual void v074(); virtual void v075(); virtual void v076(); virtual void v077(); virtual void v078(); virtual void v079(); virtual void v080(); virtual void v081(); virtual void v082(); virtual void v083(); virtual void v084(); virtual void v085(); virtual void v086(); virtual void v087(); virtual void v088(); virtual void v089(); virtual void v090(); virtual void v091(); virtual void v092(); virtual void v093(); virtual void v094(); virtual void v095(); virtual void v096(); virtual void v097(); virtual void v098(); virtual void v099(); virtual void v100(); virtual void v101(); virtual void v102(); virtual void v103(); virtual void v104(); virtual void v105(); virtual void v106(); virtual void v107(); virtual void v108(); virtual void v109(); virtual void v110(); virtual void v111(); virtual void v112(); virtual void v113(); virtual void v114(); virtual void v115(); virtual void v116(); virtual void v117(); virtual void v118(); virtual void v119(); virtual void v120(); virtual void v121(); virtual void v122(); virtual void v123(); virtual void v124(); virtual void v125(); virtual void v126(); virtual void v127(); virtual void v128(); virtual void v129(); virtual void v130(); virtual void v131(); virtual void v132(); virtual void v133(); virtual void v134(); virtual void v135(); virtual void v136(); virtual void v137(); virtual void v138(); virtual void v139(); virtual void v140(); virtual void v141(); virtual void v142(); virtual void v143(); virtual void v144(); virtual void v145(); virtual void v146();
                virtual ZTHelper73* helper(); };           // slot 147 (+0x24C)
extern char g_638690;
#define HELPER_CALL(cls, method)                                                \
    struct cls : ZTV147 { BYTE m_unk04[0x128 - 4]; ZTOwner73* m_unk128; int f(); }; \
    int cls::f()                                                                \
    {                                                                           \
        ZTHelper73* h = helper();                                               \
        ZTOwner73* o = m_unk128;                                                \
        if (!o || !o->isKindOf(&g_638690))                                      \
            o = 0;                                                              \
        int r = 0;                                                              \
        if (h && o)                                                             \
            r = h->method(o->m_unk1EC, 1);                                      \
        return r;                                                               \
    }
HELPER_CALL(Z_43888E, m4388d7)
HELPER_CALL(Z_43C175, m43c376)

// ---- 76: is the parameter name "fMoveSlow" / "fMoveFast"?
#define NAME_IS(cls, text)                                                      \
    extern const char text[];                                                   \
    struct cls { bool f(const _STL::string& name); };                          \
    bool cls::f(const _STL::string& name) { return name == text; }
NAME_IS(Z_4A9B8E, g_6393a4)
NAME_IS(Z_4AA02F, g_63943c)
```
