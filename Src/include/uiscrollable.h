// uiscrollable.h - second base class of the scrolling UI elements (name unknown).
#ifndef UISCROLLABLE_H
#define UISCROLLABLE_H

// at +0x35C in UIScrollingRegion / UIListBox: vptr, then three ints set to 0, 1, 0
class UIScrollBar;

class UIScrollable
{
public:
    UIScrollable() : m_unk04(0), m_unk08(1), m_scrollBar(0) {}
    virtual void scrollChanged();
    virtual void vf1(int position, int a, int b);   // slot 1 (name unknown): called by the mouse wheel handlers

    int m_unk04;
    int m_unk08;
    UIScrollBar* m_scrollBar;                       // +0x368 in the subclasses
};

#endif
