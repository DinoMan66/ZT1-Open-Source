// creates.cpp - the registered classes' factory functions (passed to the registries by BFRegistry.h).
// `return new T;` with the constructor out of line; BBT merged the constructor call into each one.
// Move each into its class's own .cpp when that class is written.
#include "registered_classes.h"

// 0X46498E  new ZTWorldMgr (size 0x218)
BFMgr* ZTWorldMgr::create() { return (BFMgr*)new ZTWorldMgr; }

// 0X510A49  new UIText (size 0x408)
UIElement* UIText::create() { return (UIElement*)new UIText; }

// 0X5205BC  new ZTMapView (size 0x5ec)
UIElement* ZTMapView::create() { return (UIElement*)new ZTMapView; }

// 0X525470  new ZTAdvTerrainMgr (size 0x1dc)
BFMgr* ZTAdvTerrainMgr::create() { return (BFMgr*)new ZTAdvTerrainMgr; }

// 0X527DC7  new ZTGameMgr (size 0x11b0)
BFMgr* ZTGameMgr::create() { return (BFMgr*)new ZTGameMgr; }

// 0X606CC4  new UIMessageQueue (size 0x45c)
UIElement* UIMessageQueue::create() { return (UIElement*)new UIMessageQueue; }

