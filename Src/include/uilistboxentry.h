// uilistboxentry.h - UIListBoxEntry: one row of a UIListBox (original: C:\aqua\src\UI\UIListBox.cpp).
// A row keeps three icons (normal, selected, grayed). Each icon is either a frame of an image that the
// helper 0x4176CE finds by file name, or, for a .tga file, a canvas the row creates itself.
// Only what the icon setters touch is laid out so far.
#ifndef UILISTBOXENTRY_H
#define UILISTBOXENTRY_H
#include <windows.h>
#include "gxcanvas.h"

class UIListBox;

// The 0x68-byte object that remembers which image an icon came from.
struct UIListBoxIconName                // name: guess (role of the member it is kept in)
{
    void f4b1e62();                     // 0x4B1E62: forgets the image
    BYTE m_unk00[0x68];
};

// 0x4176CE: looks the file name up and points *frame at the matching frame; false when it is not found.
bool f4176ce(RECT** frame, UIListBoxIconName* name, const char* file);

class UIListBoxEntry
{
public:
    void setNormalIcon(const char* name);      // 0x417E94
    void setSelectedIcon(const char* name);    // 0x47098B
    void setGrayedIcon(const char* name);      // 0x474C26
    void f417c8c();                            // 0x417C8C: lays the row out again after its height changed

    UIListBox* m_owner;                        // +0x00
    BYTE m_unk04[0x20];
    int m_unk24;                               // +0x24: row height, the tallest icon so far
    BYTE m_unk28[4];
    RECT* m_normalFrame;                       // +0x2C
    RECT* m_selectedFrame;                     // +0x30
    RECT* m_grayedFrame;                       // +0x34
    UIListBoxIconName m_normalName;            // +0x38
    UIListBoxIconName m_selectedName;          // +0xA0
    UIListBoxIconName m_grayedName;            // +0x108
    GXCanvas m_normalCanvas;                   // +0x170
    GXCanvas m_selectedCanvas;                 // +0x208
    GXCanvas m_grayedCanvas;                   // +0x2A0
};

#endif
