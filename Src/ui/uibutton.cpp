// uibutton.cpp - UIButton (original: C:\aqua\src\ui\uibutton.cpp).
#include "uiimage.h"

class UIButton : public UIImage                    // vtable 0x631A20
{
public:
    UIButton();
    UIButton(const UIButton& other);               // 0x4E9989
    virtual ~UIButton();                           // 0x4E0C63
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x4E99EE
    virtual int vslot40(int a, int b, int c, int d);

    bool m_unk35C, m_unk35D, m_unk35E, m_unk35F, m_unk360;
    bool m_unk361, m_unk362, m_unk363, m_unk364, m_unk365;
    int  m_unk368;
    int  m_repeatDelay;                            // +0x36C: 30
    int  m_repeatTime;                             // +0x370: 500
    UIControl* m_unk374;
};                                                 // size 0x378

// 0x5107EB
UIButton::UIButton()
    : m_unk35C(false), m_unk35D(false), m_unk35E(false), m_unk35F(false), m_unk360(false),
      m_unk361(false), m_unk362(false), m_unk363(false), m_unk364(false), m_unk365(false)
{
    resetImage3();
    m_unk368 = 0;
    m_repeatDelay = 30;
    m_repeatTime = 500;
    m_unk374 = 0;
}

// 0x50F8B0
UIElement* UIButton::create()
{
    return new UIButton;
}

// 0x4F14E7: passes the call on to the control at +0x374 when there is one
int UIButton::vslot40(int a, int b, int c, int d)
{
    int result = 1;
    if (m_unk374)
        result = m_unk374->vslot40(a, b, c, d);
    return result;
}

// slot 12, 0x4E99EE
UIControl* UIButton::clone()
{
    return new UIButton(*this);
}

// 0x4E9989: the repeat timing and +0x368 are not copied
UIButton::UIButton(const UIButton& other)
    : UIImage(other)
{
    m_unk35C = false;
    m_unk35D = false;
    m_unk35E = false;
    m_unk35F = false;
    m_unk360 = false;
    m_unk361 = false;
    m_unk362 = false;
    m_unk363 = false;
    m_unk364 = false;
    m_unk365 = other.m_unk365;
    m_unk374 = 0;
}

// 0x4E0C63
UIButton::~UIButton()
{
    if (m_unk374 != 0)
        m_unk374->f4e0d9a(this);
}
