// uibutton.cpp - UIButton (original: C:\aqua\src\ui\uibutton.cpp).
#include "uiimage.h"

class UIButton : public UIImage                    // vtable 0x631A20
{
public:
    UIButton();
    static UIElement* create();

    bool m_unk35C, m_unk35D, m_unk35E, m_unk35F, m_unk360;
    bool m_unk361, m_unk362, m_unk363, m_unk364, m_unk365;
    int  m_unk368;
    int  m_repeatDelay;                            // +0x36C: 30
    int  m_repeatTime;                             // +0x370: 500
    int  m_unk374;
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
