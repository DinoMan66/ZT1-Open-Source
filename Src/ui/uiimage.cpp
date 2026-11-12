// uiimage.cpp - UIImage (original: C:\aqua\src\ui\uiimage.cpp).
#include "uiimage.h"
#include "uimanager.h"

// slot 18, 0x4018D5
void UIImage::show()
{
    UIControl::show();
    if (m_unk350 && m_unk174 != 0)
    {
        m_unk174->Release();
        m_unk174 = 0;
    }
}

// slot 19, 0x41ACBB
void UIImage::hide()
{
    bool wasShown = false;
    if (m_unk350 && flagBit(0) == 1)
        wasShown = true;
    UIControl::hide();
    if (m_unk350 && wasShown)
        m_unk34F = 1;
}

extern int g_638f7c;                               // 0x638F7C: clock value of the previous vslot43 call (name unknown)
extern int g_638f8c;                               // 0x638F8C

// slot 43, 0x41ADF1: counts the timer down by the time since the previous call and calls show() when it runs out
void UIImage::vslot43(int now)
{
    if (flagBit(10) == 1 && (m_flags & 1) == 0)
    {
        if (m_unkA0 == m_unkA4)
        {
            m_unkA0--;
        }
        else
        {
            m_unkA0 = m_unkA0 - now + g_638f7c;
            if (m_unkA0 <= 0)
            {
                show();
                if (g_uiManager.m_unk0C == this)
                {
                    g_638f8c = 0;
                }
            }
        }
        g_638f7c = now;
    }
}

// slot 29, 0x442493
int UIImage::vslot29(int a, int b, int c)
{
    if ((a & 0x13) == 0 && !flagBit(2))
        g_uiManager.setFocus(this);
    return 0;
}

// slot 30, 0x44361A
int UIImage::vslot30(int a, int b, int c)
{
    UIControl::vslot30(a, b, c);
    if (g_uiManager.m_unk14 != this)
    {
        g_uiManager.f44316b(0);
        if (flagBit(15))
            g_uiManager.f44316b(this);
    }
    return 0;
}

// slot 31, 0x4435B9
int UIImage::vslot31(int a, int b, int c)
{
    UIControl::vslot31(a, b, c);
    return 0;
}
