// uieditabletext.cpp - UIEditableText (original: C:\aqua\src\ui\uieditabletext.cpp).
#include "uiimage.h"
#include "uimanager.h"

extern int g_unk638F4C;                            // 0x638F4C (default for +0x3A4)

class UIEditableText : public UIImage              // vtable 0x63193C
{
public:
    UIEditableText();
    UIEditableText(const UIEditableText& other);           // 0x6201AA
    virtual ~UIEditableText();                     // 0x502ED5
    virtual int vslot31(int a, int b, int c);      // 0x620299
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x620188
    void resetEditState();                         // inline [name invented]

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

// Both constructors (0x510CEE and 0x6201AA) start with these seven stores in this order: an inline
// helper they share.
inline void UIEditableText::resetEditState()
{
    m_unk364 = 0;
    m_unk360 = 0;
    m_unk35C = 0;
    m_unk368 = false;
    m_unk3A0 = false;
    m_unk398 = 0;
    m_unk39C = 0;
}

// 0x510CEE
UIEditableText::UIEditableText()
{
    resetEditState();
    m_unk3A4 = g_unk638F4C;
    m_unk3A1 = false;
    m_unk3A8 = false;
    setUnk34E(true);
    setFlag(0x8000, true);
    m_color = UIColor(0, 0, 0xFF);
}

// 0x510C52
UIElement* UIEditableText::create()
{
    return new UIEditableText;
}

// slot 12, 0x620188
UIControl* UIEditableText::clone()
{
    return new UIEditableText(*this);
}

// 0x6201AA: the edit state is reset, the text starts empty and nothing else is copied
UIEditableText::UIEditableText(const UIEditableText& other)
    : UIImage(other)
{
    resetEditState();
}

// 0x502ED5
UIEditableText::~UIEditableText()
{
    g_uiManager.f41ad6a(this);
}

// slot 31, 0x620299
int UIEditableText::vslot31(int a, int b, int c)
{
    UIImage::vslot31(a, b, c);
    return 0;
}
