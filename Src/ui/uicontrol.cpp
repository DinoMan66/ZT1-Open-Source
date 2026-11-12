// uicontrol.cpp - UIControl (original: C:\aqua\src\ui\uicontrol.cpp).
#include "uicontrol.h"
#include "uimanager.h"

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

// no standalone body left in zoo.exe either (BBT pasted it into its callers; name: guess)
void UIControl::markClean()
{
    setFlag(0x80, false);
}

// 0x4E0BC1
UIControl::~UIControl()
{
    g_uiManager.f4e0b8a(this);
    f4b203f(0);
}

// 0x401802 (name: guess; 75 callers)
void UIControl::markDirty()
{
    setFlag(0x80, true);
    for (UIControl* control = m_unk74; control != 0; control = control->m_unk74)
        control->setFlag(0x80, true);
}

// slot 22, 0x4425AC (hover bit set; name: guess)
void UIControl::vslot22()
{
    setFlag(4, true);
    if (m_cursor != 0)
        g_uiManager.setCursor(m_cursor, true);
    markDirty();
}

// slot 23, 0x442562 (hover bit cleared)
void UIControl::vslot23()
{
    setFlag(4, false);
    if (m_cursor != 0)
        g_uiManager.setCursor(0, true);
    markDirty();
}

// slot 26, 0x41914B
void UIControl::enable()
{
    if (!flagBit(19))
    {
        setFlag(2, false);
        markDirty();
    }
}

// slot 27, 0x419191
void UIControl::disable()
{
    setFlag(2, true);
    markDirty();
}

// slot 7, 0x4016D1
bool UIControl::vslot07()
{
    return false;
}

// slot 15, 0x446995
bool UIControl::vslot15(int a)
{
    return true;
}

// slot 16, 0x41215F
bool UIControl::vslot16(int a, int b)
{
    return true;
}

// slot 17, 0x40EAB5
void UIControl::vslot17(int a)
{
}

// slot 20, 0x443414
void UIControl::vslot20()
{
    setFlag(8, true);
    markDirty();
}

// slot 21, 0x4433D8
void UIControl::vslot21()
{
    setFlag(8, false);
    markDirty();
}

// slot 24, 0x443235
void UIControl::vslot24()
{
    setFlag(0x200, true);
    markDirty();
}

// slot 25, 0x4431F6
void UIControl::vslot25()
{
    setFlag(0x200, false);
    markDirty();
}

// slot 32, 0x41EABE
int UIControl::vslot32(int a, int b, int c)
{
    return vslot30(a, b, c);
}

// slot 33, 0x429D0F (shared by slots 33-36)
int UIControl::vslot33(int a, int b, int c)
{
    return 1;
}

// slot 38, 0x606CE7 (shared by slots 38/39)
int UIControl::vslot38(int a, int b)
{
    return 1;
}

// slot 44, 0x4422FD
UIControl* UIControl::vslot44(int x, int y)
{
    if ((m_flags & 0x131) == 0 && vslot47(x, y) == true)
        return this;
    return 0;
}

// slot 45, 0x40760C
UIControl* UIControl::vslot45(int id)
{
    if (m_unk90 == id)
        return this;
    return 0;
}

// slot 13, 0x4D5777
bool UIControl::vslot13(int a, const char* text)
{
    bool result = true;
    if (text == 0)
        text = m_unk24.c_str();
    if (text != 0 && *text != 0)
    {
        init();
        result = vslot10(a, text);
    }
    return result;
}

// slot 28, 0x5A0D64
void UIControl::vslot28(bool on)
{
    setFlag(0x80000, on);
    setFlag(2, on);
    markDirty();
}

// slot 29, 0x429D0F
int UIControl::vslot29(int a, int b, int c)
{
    return 1;
}

// slot 30, 0x44360A
int UIControl::vslot30(int a, int b, int c)
{
    g_uiManager.f443560(this);
    return 0;
}

// slot 31, 0x4435A8
int UIControl::vslot31(int a, int b, int c)
{
    g_uiManager.f443560(0);
    return 0;
}

// slot 37, 0x606CDF
int UIControl::vslot37(int a)
{
    return 1;
}

// slot 40, 0x4F14DF
int UIControl::vslot40(int a, int b, int c, int d)
{
    return 1;
}


// 0x418A49
void UIControl::f418a49(int index)
{
    if (index >= 0 && index < (int)m_unk58.size())
        f443bfc(m_unk58[index]);
}
