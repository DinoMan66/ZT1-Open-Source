// uilistbox.cpp - UIListBox (original: C:\aqua\src\ui\uilistbox.cpp).
#include <list>
#include <vector>
#include "uiimage.h"
#include "uiscrollable.h"

class UIListBox : public UIImage, public UIScrollable  // vtables 0x630EA4 / 0x635570
{
public:
    UIListBox();
    static UIElement* create();
    virtual void scrollChanged();

    int  m_unk36C;
    int  m_unk370;
    int  m_unk374;
    int  m_unk378;
    int  m_unk37C;
    int  m_unk380;
    int  m_unk384;
    BYTE m_unk388[0x10];
    bool m_unk398;
    int  m_unk39C;
    int  m_unk3A0;
    bool m_unk3A4;
    bool m_unk3A5;
    bool m_unk3A6;
    bool m_unk3A7, m_unk3A8, m_unk3A9, m_unk3AA, m_unk3AB, m_unk3AC;
    BYTE m_unk3AD[0x13];
    _STL::list<void*> m_items;                     // +0x3C0
    _STL::vector<void*> m_unk3C4;                  // +0x3C4
};                                                 // size 0x3D0

// 0x5119EA
UIListBox::UIListBox()
    : m_unk3A7(false), m_unk3A8(false), m_unk3A9(false), m_unk3AA(false), m_unk3AB(false),
      m_unk3AC(false)
{
    m_unk36C = 0;
    m_unk370 = 0;
    m_unk374 = 0;
    m_unk37C = -1;
    m_unk378 = -1;
    m_unk380 = 0;
    m_unk384 = 0;
    m_unk398 = false;
    m_unk39C = 0;
    m_unk3A0 = -1;
    m_unk3A4 = false;
    m_unk34E = true;
    m_unk350 = false;
    setFlag(0x8000, true);
    resetImage4();
}

// 0x511357
UIElement* UIListBox::create()
{
    return (UIImage*)new UIListBox;
}
