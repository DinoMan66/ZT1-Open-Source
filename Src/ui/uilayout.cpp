// uilayout.cpp - UILayout (original: C:\aqua\src\ui\uilayout.cpp).
#include <list>
#include "uicontrol.h"

class UILayout : public UIControl                  // vtable 0x630DDC
{
public:
    UILayout();
    static UIElement* create();

    _STL::list<void*> m_children;                  // +0xB8
    int  m_unkBC;
    int  m_unkC0;
    bool m_unkC4;
    bool m_unkC5;
};                                                 // size 0xC8

// 0x50F9DF
UILayout::UILayout()
{
    m_unkC4 = false;
    m_unkC5 = false;
    m_unkBC = 0;
    m_unkC0 = 0;
}

// 0x50FA37
UIElement* UILayout::create()
{
    return new UILayout;
}
