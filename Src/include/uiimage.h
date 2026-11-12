// uiimage.h - UIImage (original: C:\aqua\src\ui\uiimage.cpp). Placeholder layout: only what the written
// code touches. Size 0x35C (from UIImage::create, 0x50FFD8).
#ifndef UIIMAGE_H
#define UIIMAGE_H
#include "uicontrol.h"

class UIImage : public UIControl                   // vtable 0x6313E4
{
public:
    UIImage();                                     // 0x50FE83
    UIImage(const UIImage& other);                 // 0x4E95EA
    virtual ~UIImage();
    virtual void show();                           // slot 18, 0x4018D5
    virtual void hide();                           // slot 19, 0x41ACBB
    virtual void vslot43(int now);                 // 0x41ADF1
    virtual int vslot29(int a, int b, int c);      // 0x442493
    virtual int vslot30(int a, int b, int c);      // 0x44361A
    virtual int vslot31(int a, int b, int c);      // 0x4435B9
    void resetImage();                             // 0x4D3ADD (name unknown)
    void resetImage2();                            // 0x4D3DE0 (name unknown)
    void resetImage3();                            // 0x4D3635 (name unknown)
    void resetImage4();                            // 0x4D38FA (name unknown)
    void resetImage5();                            // 0x4D38B9 (name unknown)
    // inline, name unknown: UIEditableText and UIGraph only match when their constructors set +0x34E through
    // an inline call (VC6's inline budget, MATCHING_NOTES 66)
    void setUnk34E(bool on) { m_unk34E = on; }

    BYTE m_unkB8[0xBC];
    IUnknown* m_unk174;                            // +0x174: a DirectDraw surface (released through its vtable)
    BYTE m_unk178[0x1D6];
    bool m_unk34E;                                 // +0x34E
    BYTE m_unk34F;
    bool m_unk350;                                 // +0x350
    BYTE m_unk351[0x0B];
};

#endif
