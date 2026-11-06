// registered_classes.h - placeholder declarations of the self-registering classes (only the
// members BFRegistry.h needs). Replace each with the real class header when that class is written.
#ifndef REGISTERED_CLASSES_H
#define REGISTERED_CLASSES_H
#include "BFRegistry.h"

#define BF_REG_STUB(cls, base) \
    class cls { public: static const char s_className[]; static bool s_registered; static base* create(); }
// classes whose create() is known: size from `new`, constructor out of line
#define BF_REG_SIZED(cls, base, size) \
    class cls { public: cls(); static const char s_className[]; static bool s_registered; static base* create(); \
                char m_data[size]; }
BF_REG_STUB(DX8SndMgr, BFMgr);
BF_REG_STUB(ZTAIMgr, BFMgr);
BF_REG_SIZED(ZTAdvTerrainMgr, BFMgr, 0x1dc);
BF_REG_SIZED(ZTGameMgr, BFMgr, 0x11b0);
BF_REG_STUB(ZTHabitatMgr, BFMgr);
BF_REG_STUB(ZTMarketingMgr, BFMgr);
BF_REG_STUB(ZTMegatileMgr, BFMgr);
BF_REG_STUB(ZTResearchMgr, BFMgr);
BF_REG_STUB(ZTScenarioMgr, BFMgr);
BF_REG_STUB(ZTScriptMgr, BFMgr);
BF_REG_STUB(ZTShowMgr, BFMgr);
BF_REG_STUB(ZTThoughtMgr, BFMgr);
BF_REG_SIZED(ZTWorldMgr, BFMgr, 0x218);
BF_REG_SIZED(UIButton, UIElement, 0x378);
BF_REG_SIZED(UIEditableText, UIElement, 0x3ac);
BF_REG_SIZED(UIGraph, UIElement, 0x3f4);
BF_REG_STUB(UIImage, UIElement);
BF_REG_SIZED(UIImageSet, UIElement, 0x360);
BF_REG_SIZED(UILayout, UIElement, 0xc8);
BF_REG_SIZED(UIListBox, UIElement, 0x3d0);
BF_REG_SIZED(UIMessageQueue, UIElement, 0x45c);
BF_REG_SIZED(UIRadioSet, UIElement, 0xc8);
BF_REG_SIZED(UIScrollBar, UIElement, 0x4fc);
BF_REG_SIZED(UIScrollingRegion, UIElement, 0x3a0);
BF_REG_SIZED(UIStatusImage, UIElement, 0x37c);
BF_REG_SIZED(UIText, UIElement, 0x408);
BF_REG_SIZED(UIView, UIElement, 0x35c);
BF_REG_SIZED(ZTMapView, UIElement, 0x5ec);
BF_REG_STUB(ZTMessageQueue, UIElement);
BF_REG_SIZED(ZTMiniMap, UIElement, 0x3c0);

#endif
