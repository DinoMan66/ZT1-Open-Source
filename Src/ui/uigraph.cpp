// uigraph.cpp - UIGraph (original: C:\aqua\src\ui\uigraph.cpp).
#include "uigraph.h"

// merged into create() by BBT
UIGraph::UIGraph()
    : m_unk368(0)
{
    setUnk34E(true);
    init();
}

// 0x51A7C3
UIElement* UIGraph::create()
{
    return (UIElement*)new UIGraph;
}

// slot 12, 0x623678
UIControl* UIGraph::clone()
{
    return new UIGraph(*this);
}
