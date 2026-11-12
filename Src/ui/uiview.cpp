// uiview.cpp - UIView (original: C:\aqua\src\ui\uiview.cpp).
#include "uiimage.h"
#include "uimanager.h"

class UIView : public UIImage                      // vtable 0x6314C8
{
public:
    UIView();
    UIView(const UIView& other);                  // 0x620A90
    virtual ~UIView();                             // 0x502754
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x60A8D2
};                                                 // size 0x35C

// 0x52059C
UIView::UIView()
{
    setUnk34E(false);
    m_unk350 = false;
}

// 0x502754
UIView::~UIView()
{
}

// 0x604465
UIElement* UIView::create()
{
    return new UIView;
}

// slot 12, 0x60A8D2
UIControl* UIView::clone()
{
    return new UIView(*this);
}

// 0x620A90
UIView::UIView(const UIView& other)
    : UIImage(other)
{
}
