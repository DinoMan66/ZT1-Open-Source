# Removed: Src/misc/smallpairs3.cpp

Removed on 2026-10-27 because it does not meet Notes/READABILITY_STANDARD.md:

- descriptive names: invented per-function types: 2, e.g. Z_410642, Z_410FF9
- descriptive names: one-letter method names: f

The functions below MATCHED the original with this code, so the notes keep exactly what is known:
address, the placeholder name, and the matching source shape. Use them when the function is
decompiled again with real names (rename only - names never change the generated code).

## Functions (2)

| Address | Placeholder name | Recorded status |
|---|---|---|
| 0x410642 | `?f@Z_410642@@QAEPAXXZ` | matched (zoo.map) |
| 0x410ff9 | `?f@Z_410FF9@@QAEPAXXZ` | matched (zoo.map) |

## Matching source per function

### 0x410642 `?f@Z_410642@@QAEPAXXZ`

```cpp
struct Z_410642 : ZTV146
{
    BYTE m_unk04[0x251 - 4];
    bool m_unk251;                                           // +0x251
    BYTE m_unk252[2];
    unsigned short m_unk254;                                 // +0x254
    void* m40f8ac();
    void* f();
};

void* Z_410642::f()
{
    void* tile = m40f8ac();
    void* r = 0;
    if (m_unk251) {
        ZTRecA0* rec = g_639008->m41ebfd(m_unk254);
        if (rec) {
            r = rec->m_unkA0;
            if (r)
                return r;
        }
    }
    if (!tile)
        return r;
    return placeOn(tile);
}
```

### 0x410ff9 `?f@Z_410FF9@@QAEPAXXZ`

```cpp
struct Z_410FF9 : Z_410642 { void* f(); };

void* Z_410FF9::f() { return Z_410642::f(); }
```

## Full original file (reference only, not compiled)

```cpp
// smallpairs3.cpp - functions written once and shared by a one-jmp wrapper (clusters.md 62).
// Names are placeholders Z_<address>.
typedef unsigned char BYTE;

// ---- 62: the object this entity is placed on: its owner record's object if it has one, else slot 146(tile)
struct ZTRecA0 { BYTE m_unk00[0xa0]; void* m_unkA0; };
struct ZTMgr639008 { ZTRecA0* m41ebfd(unsigned short key); };
extern ZTMgr639008* g_639008;
struct ZTV146 { virtual void v000(); virtual void v001(); virtual void v002(); virtual void v003(); virtual void v004(); virtual void v005(); virtual void v006(); virtual void v007(); virtual void v008(); virtual void v009(); virtual void v010(); virtual void v011(); virtual void v012(); virtual void v013(); virtual void v014(); virtual void v015(); virtual void v016(); virtual void v017(); virtual void v018(); virtual void v019(); virtual void v020(); virtual void v021(); virtual void v022(); virtual void v023(); virtual void v024(); virtual void v025(); virtual void v026(); virtual void v027(); virtual void v028(); virtual void v029(); virtual void v030(); virtual void v031(); virtual void v032(); virtual void v033(); virtual void v034(); virtual void v035(); virtual void v036(); virtual void v037(); virtual void v038(); virtual void v039(); virtual void v040(); virtual void v041(); virtual void v042(); virtual void v043(); virtual void v044(); virtual void v045(); virtual void v046(); virtual void v047(); virtual void v048(); virtual void v049(); virtual void v050(); virtual void v051(); virtual void v052(); virtual void v053(); virtual void v054(); virtual void v055(); virtual void v056(); virtual void v057(); virtual void v058(); virtual void v059(); virtual void v060(); virtual void v061(); virtual void v062(); virtual void v063(); virtual void v064(); virtual void v065(); virtual void v066(); virtual void v067(); virtual void v068(); virtual void v069(); virtual void v070(); virtual void v071(); virtual void v072(); virtual void v073(); virtual void v074(); virtual void v075(); virtual void v076(); virtual void v077(); virtual void v078(); virtual void v079(); virtual void v080(); virtual void v081(); virtual void v082(); virtual void v083(); virtual void v084(); virtual void v085(); virtual void v086(); virtual void v087(); virtual void v088(); virtual void v089(); virtual void v090(); virtual void v091(); virtual void v092(); virtual void v093(); virtual void v094(); virtual void v095(); virtual void v096(); virtual void v097(); virtual void v098(); virtual void v099(); virtual void v100(); virtual void v101(); virtual void v102(); virtual void v103(); virtual void v104(); virtual void v105(); virtual void v106(); virtual void v107(); virtual void v108(); virtual void v109(); virtual void v110(); virtual void v111(); virtual void v112(); virtual void v113(); virtual void v114(); virtual void v115(); virtual void v116(); virtual void v117(); virtual void v118(); virtual void v119(); virtual void v120(); virtual void v121(); virtual void v122(); virtual void v123(); virtual void v124(); virtual void v125(); virtual void v126(); virtual void v127(); virtual void v128(); virtual void v129(); virtual void v130(); virtual void v131(); virtual void v132(); virtual void v133(); virtual void v134(); virtual void v135(); virtual void v136(); virtual void v137(); virtual void v138(); virtual void v139(); virtual void v140(); virtual void v141(); virtual void v142(); virtual void v143(); virtual void v144(); virtual void v145();
                virtual void* placeOn(void* tile); };          // slot 146 (+0x248)
struct Z_410642 : ZTV146
{
    BYTE m_unk04[0x251 - 4];
    bool m_unk251;                                           // +0x251
    BYTE m_unk252[2];
    unsigned short m_unk254;                                 // +0x254
    void* m40f8ac();
    void* f();
};
void* Z_410642::f()
{
    void* tile = m40f8ac();
    void* r = 0;
    if (m_unk251) {
        ZTRecA0* rec = g_639008->m41ebfd(m_unk254);
        if (rec) {
            r = rec->m_unkA0;
            if (r)
                return r;
        }
    }
    if (!tile)
        return r;
    return placeOn(tile);
}
struct Z_410FF9 : Z_410642 { void* f(); };
void* Z_410FF9::f() { return Z_410642::f(); }
```
