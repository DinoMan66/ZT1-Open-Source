// uiscrollbar.cpp - UIScrollBar (original: C:\aqua\src\ui\uiscrollbar.cpp).
#include "uiscrollbar.h"

// 0x511212
UIScrollBar::UIScrollBar()
{
    m_unk4F8 = 0;
    m_unk35C = 0;
    m_range = 100;
    m_unk364 = 0;
    m_step = 10;
    m_unk4E8 = false;
    m_unk4EC = 0;
    m_repeatDelay = 30;
    m_repeatTime = 500;
    setUnk34E(true);
    m_unk350 = false;
    resetImage5();
}

// 0x5111CB
UIElement* UIScrollBar::create()
{
    return new UIScrollBar;
}

// slot 23, 0x4E234D
void UIScrollBar::vslot23()
{
    UIControl::vslot23();
    m_upArrow.f40165f(0, false);
    m_downArrow.f40165f(0, false);
    m_thumb.f40165f(0, false);
}
