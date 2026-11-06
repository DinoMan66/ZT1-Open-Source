// uiradioset.cpp - UIRadioSet (original: C:\aqua\src\ui\uiradioset.cpp).
#include <list>
#include "uicontrol.h"

class UIRadioSet : public UIControl
{
public:
    UIRadioSet();
    static UIElement* create();

    _STL::list<void*> m_buttons;                   // +0xB8
    _STL::list<void*> m_groups;                    // +0xBC
    int m_unkC0;
    int m_unkC4;
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
