// uiscrollbar.h - UIScrollBar (original: C:\aqua\src\ui\uiscrollbar.cpp).
#ifndef UISCROLLBAR_H
#define UISCROLLBAR_H
#include "uiimage.h"

class UIScrollBarPart                              // 0x68 bytes, ctor 0x40E420 (type unknown)
{
public:
    UIScrollBarPart();
    void f40165f(int a, bool b);                   // 0x40165F
    BYTE m_data[0x68];
};

class UIScrollBar : public UIImage                 // vtable 0x631690
{
public:
    UIScrollBar();
    static UIElement* create();
    virtual void vslot23();                        // 0x4E234D
    void f41755a();                                // 0x41755A: clamps m_unk364 to the range and refreshes the thumb (name unknown)

    int  m_unk35C;                                 // +0x35C: lower end of the range (0)
    int  m_range;                                  // +0x360: 100
    int  m_unk364;                                 // +0x364: current position
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

#endif
