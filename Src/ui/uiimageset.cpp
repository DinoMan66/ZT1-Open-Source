// uiimageset.cpp - UIImageSet (original: C:\aqua\src\ui\uiimageset.cpp).
#include "uiimage.h"

class UIImageSet : public UIImage                  // vtable 0x6315AC
{
public:
    UIImageSet();
    static UIElement* create();

    int m_current;                                 // +0x35C: -1 = none
};                                                 // size 0x360

// 0x512259
UIImageSet::UIImageSet()
{
    m_current = -1;
}

// 0x512275
UIElement* UIImageSet::create()
{
    return new UIImageSet;
}
