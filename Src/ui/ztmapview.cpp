// ztmapview.cpp - ZTMapView (the screen control cached by 0x4017E5).
#include "ztmapview.h"

ZTMapView* UIH_4017E5();                           // uiscreenhandlers.cpp: the cached screen with id 0x1B58

// 0x4E0E8F
// defined out of line: BBT pastes this body into the handlers that call it (MATCHING_NOTES 95)
void ZTMapView::setUnk364(UIControl* control)
{
    m_unk364 = control;
}

// 0x410F84: the selected entity of the cached screen (0 when there is no screen)
// defined out of line: 41 handlers call it
ZTEntity* f410f84()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        return view->m_unk438;
    return 0;
}

// 0x4EF75B
void f4ef75b(int a, int b)
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4b2322(a, b);
}
