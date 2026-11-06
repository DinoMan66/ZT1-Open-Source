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
    static UIElement* create();

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
    m_unk34E = true;
}

// 0x520D1C
UIElement* ZTMiniMap::create()
{
    return (UIElement*)new ZTMiniMap;
}
