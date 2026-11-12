// uiradioset.cpp - UIRadioSet (original: C:\aqua\src\ui\uiradioset.cpp).
#include <list>
#include "uicontrol.h"

class UIRadioSet : public UIControl
{
public:
    UIRadioSet();
    static UIElement* create();
    virtual void vslot11(int a, int b);            // 0x401115
    virtual int vslot40(int a, int b, int c, int d); // 0x4F1515

    _STL::list<void*> m_buttons;                   // +0xB8
    _STL::list<void*> m_groups;                    // +0xBC
    int m_unkC0;
    UIControl* m_unkC4;
};                                                 // size 0xC8

// merged into create() by BBT
UIRadioSet::UIRadioSet()
    : m_unkC0(0), m_unkC4(0)
{
    setFlag(1, true);
}

// 0x5114FB
UIElement* UIRadioSet::create()
{
    return (UIElement*)new UIRadioSet;
}

// slot 40, 0x4F1515: passes the call on to the control at +0xC4 when there is one
int UIRadioSet::vslot40(int a, int b, int c, int d)
{
    int result = 1;
    if (m_unkC4)
        result = m_unkC4->vslot40(a, b, c, d);
    return result;
}

// slot 11, 0x401115: does nothing
void UIRadioSet::vslot11(int a, int b)
{
}
