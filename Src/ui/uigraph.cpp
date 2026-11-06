// uigraph.cpp - UIGraph (original: C:\aqua\src\ui\uigraph.cpp).
#include <map>
#include <string>
#include "uiimage.h"

struct UIGraphSeries { int unk[5]; };              // map value: node size 0x28

struct UIGraphFlags
{
    UIGraphFlags()
    {
        m_show00 = false;
        m_show01 = false;
        m_show02 = false;
        m_show03 = false;
        m_show04 = false;
        m_show05 = false;
        m_show06 = false;
        m_show07 = false;
        m_show08 = false;
        m_show09 = false;
        m_show10 = false;
        m_show11 = false;
        m_show12 = false;
        m_show13 = false;
        m_show14 = false;
        m_show15 = false;
        m_show16 = false;
        m_show17 = false;
        m_show18 = false;
        m_show19 = false;
        m_show20 = false;
        m_show21 = false;
        m_show22 = false;
        m_show23 = false;
    }
    bool m_show00, m_show01, m_show02, m_show03, m_show04, m_show05, m_show06, m_show07, m_show08, m_show09, m_show10, m_show11;
    bool m_show12, m_show13, m_show14, m_show15, m_show16, m_show17, m_show18, m_show19, m_show20, m_show21, m_show22, m_show23;
};

class UIGraph : public UIImage
{
public:
    UIGraph();
    static UIElement* create();
    void init();                                   // 0x51A646

    _STL::map<int, UIGraphSeries> m_series;        // +0x35C
    int  m_unk368;
    int  m_unk36C[25];
    _STL::string m_title;                          // +0x3D0
    UIGraphFlags m_flags;                          // +0x3DC (24 bools)
};                                                 // size 0x3F4

// merged into create() by BBT
UIGraph::UIGraph()
    : m_unk368(0)
{
    m_unk34E = true;
    init();
}

// 0x51A7C3
UIElement* UIGraph::create()
{
    return (UIElement*)new UIGraph;
}
