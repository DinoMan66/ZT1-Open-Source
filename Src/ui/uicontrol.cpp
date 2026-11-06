// uicontrol.cpp - UIControl (original: C:\aqua\src\ui\uicontrol.cpp).
#include "uicontrol.h"

// 0x50F8E7
UIControl::UIControl()
{
    m_unk74 = 0;
    m_flags = 1;
    m_unk90 = 0;
    m_unk80 = 0;
    m_unk78 = 0;
    m_unk48 = false;
    init();
}

// no standalone body left in zoo.exe: BBT inlined all 185 calls
void UIControl::setFlag(DWORD flag, bool on)
{
    if (on == true)
        m_flags |= flag;
    else
        m_flags &= ~flag;
}
