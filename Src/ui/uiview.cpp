// uiview.cpp - UIView (original: C:\aqua\src\ui\uiview.cpp).
#include "uiimage.h"

class UIView : public UIImage                      // vtable 0x6314C8
{
public:
    UIView();
    static UIElement* create();
};                                                 // size 0x35C

// 0x52059C
UIView::UIView()
{
    m_unk34E = false;
    m_unk350 = false;
}

// 0x604465
UIElement* UIView::create()
{
    return new UIView;
}
