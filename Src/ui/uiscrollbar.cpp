// uiscrollbar.cpp - UIScrollBar (original: C:\aqua\src\ui\uiscrollbar.cpp).
#include "uiimage.h"

class UIScrollBarPart                              // 0x68 bytes, ctor 0x40E420 (type unknown)
{
public:
    UIScrollBarPart();
    BYTE m_data[0x68];
};

class UIScrollBar : public UIImage                 // vtable 0x631690
{
public:
    UIScrollBar();
    static UIElement* create();

    int  m_unk35C;
    int  m_range;                                  // +0x360: 100
    int  m_unk364;
    int  m_step;                                   // +0x368: 10
    BYTE m_unk36C[0x1C];
    UIScrollBarPart m_upArrow;                     // +0x388
    UIScrollBarPart m_downArrow;                   // +0x3F0
    UIScrollBarPart m_thumb;                       // +0x458
    BYTE m_unk4C0[0x28];
    bool m_unk4E8;
    int  m_unk4EC;
    int  m_repeatDelay;                            // +0x4F0: 30
    int  m_repeatTime;                             // +0x4F4: 500
    int  m_unk4F8;
};                                                 // size 0x4FC

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
    m_unk34E = true;
    m_unk350 = false;
    resetImage5();
}

// 0x5111CB
UIElement* UIScrollBar::create()
{
    return new UIScrollBar;
}
