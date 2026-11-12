// uilayout.cpp - UILayout (original: C:\aqua\src\ui\uilayout.cpp).
#include <list>
#include "uicontrol.h"

class UILayout : public UIControl                  // vtable 0x630DDC
{
public:
    UILayout();
    virtual ~UILayout();                           // 0x502353
    static UIElement* create();
    virtual bool vslot14();                        // 0x4D4997
    virtual bool vslot15(int a);                   // 0x47ABB1
    virtual bool vslot16(int a, int b);            // 0x592B03
    virtual int vslot30(int a, int b, int c);      // 0x58C8B4
    virtual int vslot31(int a, int b, int c);      // 0x58C88E
    virtual void show();                           // 0x443B70
    virtual int vslot34(int a, int b, int c);      // 0x58CE2E

    _STL::list<UIControl*> m_children;                  // +0xB8
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

// slot 31, 0x58C88E
int UILayout::vslot31(int a, int b, int c)
{
    UIControl::vslot31(a, b, c);
    m_unkC4 = false;
    return 0;
}

// slot 34, 0x58CE2E
void UILayout::show()
{
    for (_STL::list<UIControl*>::iterator it = m_children.begin(); it != m_children.end(); ++it)
    {
        (*it)->show();
    }
    UIControl::show();
}

int UILayout::vslot34(int a, int b, int c)
{
    m_unk40 = m_unk30;
    m_unk44 = m_unk34;
    m_unk48 = false;
    return 0;
}

// 0x502353: deletes the children; each one unlinks itself from m_children (setParent 0x4B203F)
UILayout::~UILayout()
{
    while (!m_children.empty())
    {
        UIControl* child = m_children.front();
        child->f4b203f(0);
        delete child;
    }
}

// slot 14, 0x4D4997: the layout's own answer, cleared if any child says no
bool UILayout::vslot14()
{
    bool result = UIControl::vslot14();
    for (_STL::list<UIControl*>::iterator it = m_children.begin(); it != m_children.end(); ++it)
    {
        if (!(*it)->vslot14())
            result = false;
    }
    return result;
}

// slot 15, 0x47ABB1: true only when every child answers true
bool UILayout::vslot15(int a)
{
    bool result = true;
    for (_STL::list<UIControl*>::iterator it = m_children.begin(); it != m_children.end(); ++it)
        result &= (*it)->vslot15(a);
    return result;
}

// slot 16, 0x592B03: true only when every child answers true
bool UILayout::vslot16(int a, int b)
{
    bool result = true;
    for (_STL::list<UIControl*>::iterator it = m_children.begin(); it != m_children.end(); ++it)
        result &= (*it)->vslot16(a, b);
    return result;
}

// slot 30, 0x58C8B4
int UILayout::vslot30(int a, int b, int c)
{
    UIControl::vslot30(a, b, c);
    if (m_unk74 != 0)
        m_unk74->f41aeb1(this);
    m_unkC0 = c;
    m_unkBC = b;
    m_unkC4 = true;
    return 0;
}
