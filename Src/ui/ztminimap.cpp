// ztminimap.cpp - ZTMiniMap (original: C:\aqua\src\zt\ztminimap.cpp ?).
#include <limits.h>
#include <map>
#include <vector>
#include "uiimage.h"

struct ZTMiniMapEntry { int unk[3]; };             // map value: node size 0x20

struct ZTMiniMapStats
{
    ZTMiniMapStats() : v0(0), v1(0), v2(0), v3(0), v4(0), v5(0), v6(0), v7(0), v8(0) {}
    int v0, v1, v2, v3, v4, v5, v6, v7, v8;
};

struct ZTMiniMapMore
{
    ZTMiniMapMore() : v0(0), v1(0), v2(0) {}
    int v0, v1, v2;
};

class ZTMiniMap : public UIImage
{
public:
    ZTMiniMap();
    ZTMiniMap(const ZTMiniMap& other);                // 0x619477
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x6198D7
    virtual void vslot56(int a);                   // 0x4B2477

    int  m_unk35C;
    int  m_unk360;
    ZTMiniMapStats m_stats;                        // +0x364
    ZTMiniMapMore m_more;
    bool m_unk394;
    int  m_minX, m_maxX, m_minY, m_maxY;           // +0x398
    _STL::vector<void*> m_unk3A8;                  // +0x3A8
    _STL::map<int, ZTMiniMapEntry> m_unk3B4;       // +0x3B4
};                                                 // size 0x3C0

// merged into create() by BBT
ZTMiniMap::ZTMiniMap()
    : m_unk394(false), m_minX(INT_MIN), m_maxX(INT_MAX), m_minY(INT_MIN), m_maxY(INT_MAX)
{
    // a plain store here: setUnk34E() would change what VC6 inlines (MATCHING_NOTES 66)
    m_unk34E = true;
}

// 0x520D1C
UIElement* ZTMiniMap::create()
{
    return (UIElement*)new ZTMiniMap;
}

// slot 12, 0x6198D7
UIControl* ZTMiniMap::clone()
{
    return new ZTMiniMap(*this);
}

// slot 56, 0x4B2477
void ZTMiniMap::vslot56(int a)
{
    m_unk394 = true;
    UIControl::vslot56(a);
}
