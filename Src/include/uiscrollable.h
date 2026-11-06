// uiscrollable.h - second base class of the scrolling UI elements (name unknown).
#ifndef UISCROLLABLE_H
#define UISCROLLABLE_H

// at +0x35C in UIScrollingRegion / UIListBox: vptr, then three ints set to 0, 1, 0
class UIScrollable
{
public:
    UIScrollable() : m_unk04(0), m_unk08(1), m_unk0C(0) {}
    virtual void scrollChanged();

    int m_unk04;
    int m_unk08;
    int m_unk0C;
};

#endif
