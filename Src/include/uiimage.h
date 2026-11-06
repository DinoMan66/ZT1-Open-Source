// uiimage.h - UIImage (original: C:\aqua\src\ui\uiimage.cpp). Placeholder layout: only what the written
// code touches. Size 0x35C (from UIImage::create, 0x50FFD8).
#ifndef UIIMAGE_H
#define UIIMAGE_H
#include "uicontrol.h"

class UIImage : public UIControl                   // vtable 0x6313E4
{
public:
    UIImage();                                     // 0x50FE83
    virtual ~UIImage();
    void resetImage();                             // 0x4D3ADD (name unknown)
    void resetImage2();                            // 0x4D3DE0 (name unknown)
    void resetImage3();                            // 0x4D3635 (name unknown)
    void resetImage4();                            // 0x4D38FA (name unknown)
    void resetImage5();                            // 0x4D38B9 (name unknown)

    BYTE m_unkB8[0x296];
    bool m_unk34E;                                 // +0x34E
    BYTE m_unk34F;
    bool m_unk350;                                 // +0x350
    BYTE m_unk351[0x0B];
};

#endif
