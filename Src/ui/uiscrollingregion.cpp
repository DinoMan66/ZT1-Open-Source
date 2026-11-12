// uiscrollingregion.cpp - UIScrollingRegion (original: C:\aqua\src\ui\uiscrollingregion.cpp).
#include <list>
#include "uiimage.h"
#include "uiscrollable.h"
#include "uiscrollbar.h"

class UIScrollingRegion : public UIImage, public UIScrollable
{
public:
    UIScrollingRegion();
    virtual ~UIScrollingRegion();                  // 0x503003
    static UIElement* create();
    virtual void scrollChanged();
    virtual int vslot37(int a);                    // 0x622EF8
    virtual int vslot40(int a, int b, int c, int d);   // 0x4DE381
    virtual void vslot55();                        // 0x40100B
    void f622f18();                                // 0x622F18

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

// 0x503003: the member list and the UIImage base are torn down implicitly
UIScrollingRegion::~UIScrollingRegion()
{
}

// slot 40, 0x4DE381: mouse wheel; d is the wheel delta (multiples of 120), two units per notch
int UIScrollingRegion::vslot40(int a, int b, int c, int d)
{
    int result = 1;
    if (m_scrollBar != 0 && m_scrollBar->m_unk35C < m_scrollBar->m_range)
    {
        m_scrollBar->m_unk364 += (d / -120) * 2;
        m_scrollBar->f41755a();
        vf1(m_scrollBar->m_unk364, 0, 1);
        result = 0;
    }
    return result;
}

// 0x5125D8
UIElement* UIScrollingRegion::create()
{
    return (UIElement*)new UIScrollingRegion;
}

// slot 37, 0x622EF8: only the value 9 is handled here
int UIScrollingRegion::vslot37(int a)
{
    int result = 0;
    if (a == 9)
        f622f18();
    else
        result = 1;
    return result;
}

// slot 55, 0x40100B: does nothing
void UIScrollingRegion::vslot55()
{
}
