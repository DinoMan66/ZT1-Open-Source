// uistatusimage.cpp - UIStatusImage (original: C:\aqua\src\ui\uistatusimage.cpp).
#include <vector>
#include "uiimage.h"

class UIStatusImage : public UIImage
{
public:
    UIStatusImage();
    UIStatusImage(const UIStatusImage& other);     // 0x6229FF
    virtual ~UIStatusImage() {}                    // inline: the deleting destructor 0x502B10 has it expanded
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x6229DD
    virtual void vslot22();                        // 0x4EF9F1
    virtual void vslot23();                        // 0x4EFA36
    virtual void vslot55();                        // 0x4329C7
    void f4328ae(int a, int b);                    // 0x4328AE

    int m_unk35C;
    int m_unk360;
    int m_unk364;
    int m_unk368;
    int m_unk36C;
    _STL::vector<void*> m_unk370;                  // +0x370
};                                                 // size 0x37C

// merged into create() by BBT
UIStatusImage::UIStatusImage()
{
    resetImage();
    m_unk35C = 0;
    m_unk360 = 0;
    m_unk368 = 0;
    m_unk36C = 0;
    setUnk34E(true);
    m_unk364 = 100;
}

// 0x510F33
UIElement* UIStatusImage::create()
{
    return (UIElement*)new UIStatusImage;
}

// 0x4EF9F1: base focus-gained handling, then marks the control clean
void UIStatusImage::vslot22()
{
    UIControl::vslot22();
    markClean();
}

// 0x4EFA36: base focus-lost handling, then marks the control clean
void UIStatusImage::vslot23()
{
    UIControl::vslot23();
    markClean();
}

// slot 12, 0x6229DD
UIControl* UIStatusImage::clone()
{
    return new UIStatusImage(*this);
}

// 0x6229FF
UIStatusImage::UIStatusImage(const UIStatusImage& other)
    : UIImage(other)
{
    m_unk35C = other.m_unk35C;
    m_unk360 = other.m_unk360;
    m_unk364 = other.m_unk364;
    m_unk368 = other.m_unk368;
    m_unk36C = other.m_unk36C;
}

// slot 55, 0x4329C7
void UIStatusImage::vslot55()
{
    if (m_unk4C > m_unk50)
        m_unkB0 = true;
    else
        m_unkB1 = true;
    f4328ae(m_unk36C, m_unk368);
}
