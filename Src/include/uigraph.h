// uigraph.h - UIGraph (original: C:\aqua\src\ui\uigraph.cpp).
#ifndef UIGRAPH_H
#define UIGRAPH_H
#include <map>
#include <string>
#include "uiimage.h"

struct UIGraphSeries { int unk[5]; };              // map value: node size 0x28


class UIGraph : public UIImage
{
public:
    UIGraph();
    UIGraph(const UIGraph& other);                  // 0x62369A
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x623678
    void init();                                   // 0x51A646
    void f51a5ef(int mode);                        // 0x51A5EF: replaces the helper object at +0x368 for the given mode; body not written

    _STL::map<int, UIGraphSeries> m_series;        // +0x35C
    int  m_unk368;
    int  m_unk36C[25];
    _STL::string m_title;                          // +0x3D0
    UIColor m_color0;                              // +0x3DC: 8 colours, set by init() (0x51A646)
    UIColor m_color1;                              // +0x3DF
    UIColor m_color2;                              // +0x3E2
    UIColor m_color3;                              // +0x3E5
    UIColor m_color4;                              // +0x3E8
    UIColor m_color5;                              // +0x3EB
    UIColor m_color6;                              // +0x3EE
    UIColor m_color7;                              // +0x3F1
};                                                 // size 0x3F4

#endif
