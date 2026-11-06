// uistatusimage.cpp - UIStatusImage (original: C:\aqua\src\ui\uistatusimage.cpp).
#include <vector>
#include "uiimage.h"

class UIStatusImage : public UIImage
{
public:
    UIStatusImage();
    static UIElement* create();

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
    m_unk34E = true;
    m_unk364 = 100;
}

// 0x510F33
UIElement* UIStatusImage::create()
{
    return (UIElement*)new UIStatusImage;
}
