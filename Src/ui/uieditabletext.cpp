// uieditabletext.cpp - UIEditableText (original: C:\aqua\src\ui\uieditabletext.cpp).
#include "uiimage.h"

extern int g_unk638F4C;                            // 0x638F4C (default for +0x3A4)

class UIEditableText : public UIImage              // vtable 0x63193C
{
public:
    UIEditableText();
    static UIElement* create();

    int  m_unk35C;
    int  m_unk360;
    int  m_unk364;
    bool m_unk368;
    BYTE m_unk369[0x23];
    _STL::string m_text;                           // +0x38C
    int  m_unk398;
    int  m_unk39C;
    bool m_unk3A0;
    bool m_unk3A1;
    int  m_unk3A4;
    bool m_unk3A8;
};                                                 // size 0x3AC

// 0x510CEE
UIEditableText::UIEditableText()
{
    m_unk364 = 0;
    m_unk360 = 0;
    m_unk35C = 0;
    m_unk368 = false;
    m_unk3A0 = false;
    m_unk398 = 0;
    m_unk39C = 0;
    m_unk3A4 = g_unk638F4C;
    m_unk3A1 = false;
    m_unk3A8 = false;
    m_unk34E = true;
    setFlag(0x8000, true);
    m_color = UIColor(0, 0, 0xFF);
}

// 0x510C52
UIElement* UIEditableText::create()
{
    return new UIEditableText;
}
