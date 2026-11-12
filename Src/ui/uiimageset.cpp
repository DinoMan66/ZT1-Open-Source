// uiimageset.cpp - UIImageSet (original: C:\aqua\src\ui\uiimageset.cpp).
#include "uiimage.h"

class UIImageSet : public UIImage                  // vtable 0x6315AC
{
public:
    UIImageSet();
    UIImageSet(const UIImageSet& other);          // 0x622FF9
    virtual ~UIImageSet() {}                       // inline: the deleting destructor 0x503054 has it expanded
    static UIElement* create();
    virtual UIControl* clone();                    // slot 12, 0x622FD7
    virtual void vslot22();                        // 0x4426EA
    virtual void vslot23();                        // 0x44273E

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

// slot 22, 0x4426EA (keeps flag 0x80 as it was before the base call marked the control dirty)
void UIImageSet::vslot22()
{
    bool wasDirty = flagBit(7);
    UIControl::vslot22();
    if (!wasDirty)
        markClean();
}

// slot 23, 0x44273E
void UIImageSet::vslot23()
{
    bool wasDirty = flagBit(7);
    UIControl::vslot23();
    if (!wasDirty)
        markClean();
}

// slot 12, 0x622FD7
UIControl* UIImageSet::clone()
{
    return new UIImageSet(*this);
}

// 0x622FF9
UIImageSet::UIImageSet(const UIImageSet& other)
    : UIImage(other)
{
    m_current = other.m_current;
}
