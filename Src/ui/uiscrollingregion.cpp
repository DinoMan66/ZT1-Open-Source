// uiscrollingregion.cpp - UIScrollingRegion (original: C:\aqua\src\ui\uiscrollingregion.cpp).
#include <list>
#include "uiimage.h"
#include "uiscrollable.h"

class UIScrollingRegion : public UIImage, public UIScrollable
{
public:
    UIScrollingRegion();
    static UIElement* create();
    virtual void scrollChanged();

    int m_unk36C[4];                               // +0x36C
    int m_unk37C;
    int m_unk380;
    int m_unk384;
    int m_unk388;
    int m_unk38C;
    int m_unk390;
    int m_unk394[2];
    _STL::list<void*> m_children;                  // +0x39C
};                                                 // size 0x3A0

// merged into create() by BBT
UIScrollingRegion::UIScrollingRegion()
{
    resetImage2();
    m_unk350 = false;
    m_unk384 = 0;
    m_unk37C = 0;
    m_unk380 = 0;
    m_unk388 = 0;
    m_unk390 = 0;
}

// 0x5125D8
UIElement* UIScrollingRegion::create()
{
    return (UIElement*)new UIScrollingRegion;
}
