// ztmapview.h - the screen control with id 0x1B58 (cached by 0x4017E5). Placeholder layout: only the
// members and methods the written code touches. The class is the registered ZTMapView (size 0x5EC):
// its constructor 0x51F80C is the one that initialises +0x438 and +0x43C.
#ifndef ZTMAPVIEW_H
#define ZTMAPVIEW_H
#include "uicontrol.h"
#include "ztentity.h"

class ZTMapView : public UIControl                 // name: guess (constructor 0x51F80C writes +0x438 / +0x43C)
{
public:
    void f4b2322(int a, int b);                    // 0x4B2322
    void f4b06be(bool on);                         // 0x4B06BE
    void f4e1064(bool on);                         // 0x4E1064
    void f4da19c(bool on);                         // 0x4DA19C
    void f48d065(bool on);                         // 0x48D065
    void f5096e8(bool on);                         // 0x5096E8
    void f6097ef(bool on);                         // 0x6097EF
    void f4dd600(bool on);                         // 0x4DD600
    void f4dd630(bool on);                         // 0x4DD630
    void f4f189a(int a, int b, int c, int d, int e);   // 0x4F189A
    void f46ab75();                                // 0x46AB75
    void f4e5d11(int a);                           // 0x4E5D11
    int  f4da53a();                                // 0x4DA53A

    void setUnk364(UIControl* control);            // 0x4E0E8F: name unknown; BBT pastes this tiny body into its callers

    BYTE m_unkB8[0x2A8];
    void* m_unk360;
    UIControl* m_unk364;
    BYTE m_unk368[8];
    int  m_unk370;
    BYTE m_unk374[4];
    bool m_unk378;
    BYTE m_unk379[0xBF];
    ZTEntity* m_unk438;                            // the selected entity (see f410f84)
    bool m_unk43C;
};

#endif
