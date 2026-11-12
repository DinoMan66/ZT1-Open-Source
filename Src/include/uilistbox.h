// uilistbox.h - UIListBox (original: C:\aqua\src\ui\uilistbox.cpp).
#ifndef UILISTBOX_H
#define UILISTBOX_H
#include <list>
#include <vector>
#include "uiimage.h"
#include "uiscrollable.h"
#include "uiscrollbar.h"

class UIListBox : public UIImage, public UIScrollable  // vtables 0x630EA4 / 0x635570
{
public:
    UIListBox();
    static UIElement* create();
    virtual void scrollChanged();
    virtual void vslot23();                        // 0x418AF4
    virtual int vslot40(int a, int b, int c, int d);   // 0x4ED732
    virtual bool vslot47(int x, int y);            // 0x418AE2
    virtual void vslot55();                        // 0x4EC999
    void setSelectedIndex(int index, bool scroll); // 0x4189E8
    int getUnk390() const { return m_unk390; }     // inline: the icon setters copy the value (a temporary in the original)
    void* f48bce9(int* index);                     // 0x48BCE9: moves *index to the last valid item
    void f417a8e(bool flag);                       // 0x417A8E
    void f417695(int index, bool a, bool b);       // 0x417695: scrolls the item into view
    void f4f9908(int index);                       // 0x4F9908: removes the item with the given index

    int  m_unk36C;
    int  m_unk370;
    int  m_unk374;
    int  m_unk378;
    int  m_unk37C;
    int  m_unk380;
    int  m_unk384;
    int  m_unk388;
    int  m_unk38C;
    int  m_unk390;                                 // read by UIListBoxEntry::set*Icon
    int  m_unk394;
    bool m_unk398;
    int  m_unk39C;
    int  m_unk3A0;
    bool m_unk3A4;
    bool m_unk3A5;
    bool m_unk3A6;
    bool m_unk3A7, m_unk3A8, m_unk3A9, m_unk3AA, m_unk3AB, m_unk3AC;
    BYTE m_unk3AD[0x13];
    _STL::list<void*> m_items;                     // +0x3C0
    _STL::vector<void*> m_unk3C4;                  // +0x3C4
};                                                 // size 0x3D0

#endif
