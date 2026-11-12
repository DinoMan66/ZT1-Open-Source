// uilistbox.cpp - UIListBox (original: C:\aqua\src\ui\uilistbox.cpp).
#include "uilistbox.h"


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
    // a plain store here: setUnk34E() would change what VC6 inlines (MATCHING_NOTES 66)
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

// slot 23, 0x418AF4
void UIListBox::vslot23()
{
    m_unk378 = -1;
    UIControl::vslot23();
}

// slot 40, 0x4ED732: mouse wheel; d is the wheel delta (multiples of 120), two units per notch
int UIListBox::vslot40(int a, int b, int c, int d)
{
    int result = 1;
    if (m_scrollBar != 0 && m_scrollBar->m_unk35C < m_scrollBar->m_range)
    {
        vf1(m_scrollBar->m_unk364 - (d / 120) * 2, 1, 1);
        result = 0;
    }
    return result;
}

// slot 47, 0x418AE2
bool UIListBox::vslot47(int x, int y)
{
    return UIControl::vslot47(x, y);
}

// 0x4189E8: selects the item with the given index and scrolls it into view when asked to
void UIListBox::setSelectedIndex(int index, bool scroll)
{
    if (index >= (int)m_items.size())
        f48bce9(&index);
    m_unk37C = index;
    if (scroll && index >= 0 && (index < m_unk36C || index > m_unk370))
        f417695(index, true, false);
    else
        markDirty();
}

// slot 55, 0x4EC999
void UIListBox::vslot55()
{
    f417a8e(true);
}
