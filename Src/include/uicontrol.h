// uicontrol.h - UIElement (root of the UI classes) and UIControl
// (original: C:\aqua\src\ui\uielement.cpp / uicontrol.cpp). Layout from the constructors; unknown
// members are padding.
#ifndef UICONTROL_H
#define UICONTROL_H
#include <windows.h>
#include <string>
#include <vector>

struct UIColor                                     // 3 bytes
{
    UIColor() : c0(0), c1(0), c2(0) {}
    UIColor(BYTE a, BYTE b, BYTE c) : c0(a), c1(b), c2(c) {}
    BYTE c0, c1, c2;
};

class UIElement                                    // vtable 0x632258
{
public:
    UIElement() : m_unk04(1), m_unk06(0), m_id(++s_nextId) {}
    // six empty virtuals (all share the body at 0x40100C); UIElement's vtable 0x632258 has no others
    virtual void vslot00() {}
    virtual void vslot01() {}
    virtual void vslot02() {}
    virtual void vslot03() {}
    virtual void vslot04() {}
    virtual void vslot05() {}

    short m_unk04;
    short m_unk06;
    int   m_id;                                    // +0x08: unique id
    static int s_nextId;                           // 0x638D48
};

class UIControl : public UIElement                 // vtable 0x63203C
{
public:
    UIControl();                                   // 0x50F8E7
    virtual ~UIControl();                          // slot 6 (the deleting wrapper is at 0x4E0C83)

    // flag bits at +0x7C; body 0x4014AC, BBT inlined most of its 185 calls
    void setFlag(DWORD flag, bool on);
    void f4b203f(UIControl* parent);               // 0x4B203F: sets m_unk74 (the parent), unlinking from the old one
    void f4e0d9a(UIControl* other);                // 0x4E0D9A (called by the UIButton destructor on its m_unk374)
    void f506f04(int a);                           // 0x506F04 (works on +0x40 / +0x44)
    void f41aeb1(UIControl* child);                // 0x41AEB1 (called on the parent)
    void f418a49(int index);                       // 0x418A49: calls f443bfc for the item at index (m_unk58 entries); name: guess
    void f4438fb(UIControl* item);                 // 0x4438FB (name: guess; body not written)
    void f443bfc(void* item);                      // 0x443BFC: stores item in m_unk54 (logs); body not written
    void f4b1aa0(const char* text, bool flag);     // 0x4B1AA0: body not written
    void markClean();    // name: guess (counterpart of markDirty)
    void markDirty();                              // 0x401802: sets flag 0x80 on this control and its parents (name: guess)
    bool flagBit(int bit) const { return (m_flags >> bit) & 1; }   // inline accessor (shr + test cl,1)

    // virtual slots the UI handlers call (names are guesses; slot = offset / 4)
    virtual bool vslot07();                        // 0x4016D1: returns false
    virtual bool vslot08();
    virtual void vslot09();
    virtual bool vslot10(int a, const char* text); // pure in UIControl (0x629B58 is the CRT's _purecall)
    virtual void vslot11(int a, int b);            // _purecall in UIControl; UIRadioSet 0x401115 is `ret 8`
    virtual UIControl* clone();                    // slot 12 (name: guess; the overrides are `new T(*this)`). _purecall in the original's vtable
    virtual bool vslot13(int a, const char* text);
    virtual bool vslot14();                        // 0x4D4909
    virtual bool vslot15(int a);                   // 0x446995: returns true
    virtual bool vslot16(int a, int b);            // 0x41215F: returns true
    virtual void vslot17(int a);                   // 0x40EAB5: does nothing
    virtual void show();                           // slot 18 (+0x48)
    virtual void hide();                           // slot 19 (+0x4C); bit 1 of m_flags = shown
    virtual void vslot20();
    virtual void vslot21();                        // +0x54
    virtual void vslot22();
    virtual void vslot23();
    virtual void vslot24();
    virtual void vslot25();
    virtual void enable();                         // slot 26 (+0x68)
    virtual void disable();                        // slot 27 (+0x6C)
    virtual void vslot28(bool on);
    virtual int vslot29(int a, int b, int c);
    virtual int vslot30(int a, int b, int c);
    virtual int vslot31(int a, int b, int c);
    virtual int vslot32(int a, int b, int c);
    virtual int vslot33(int a, int b, int c);      // slots 33-36 share one body (0x429D0F): return 1
    virtual int vslot34(int a, int b, int c);
    virtual void vslot35();
    virtual void vslot36();
    virtual int vslot37(int a);                    // 0x606CDF: returns 1
    virtual int vslot38(int a, int b);             // slots 38/39 share one body (0x606CE7): return 1
    virtual void vslot39();
    virtual int vslot40(int a, int b, int c, int d); // 0x4F14DF: returns 1
    virtual void vslot41();
    virtual void vslot42();
    virtual void vslot43(int now);                 // per-frame timer (UIImage: 0x41ADF1)
    virtual UIControl* vslot44(int x, int y);      // returns this when the point hits (and the control is active)
    virtual UIControl* vslot45(int id);            // returns this when m_unk90 == id
    virtual void vslot46();
    virtual bool vslot47(int x, int y);
    virtual void init();                           // slot 48, 0x4D2EDB (name unknown)
    virtual void setText(_STL::string text, int a);   // slot 49 (+0xC4)
    virtual void vslot50(int id, int a);           // slot 50 (+0xC8): set a string/image by id?
    virtual void vslot51();
    virtual void vslot52();
    virtual void vslot53();
    virtual void vslot54();
    virtual void vslot55();                        // UIListBox: 0x4EC999
    virtual void vslot56(int a);                   // 0x41BCE8

    _STL::string m_name;                           // +0x0C
    _STL::string m_unk18;                          // +0x18
    _STL::string m_unk24;                          // +0x24
    int   m_unk30;
    int   m_unk34;
    int   m_unk38;
    int   m_unk3C;
    int   m_unk40;
    int   m_unk44;
    bool  m_unk48;                                 // +0x48
    BYTE  m_unk49[3];
    int   m_unk4C;
    int   m_unk50;
    BYTE  m_unk54[4];
    _STL::vector<void*> m_unk58;                   // +0x58
    BYTE  m_unk64[0x10];
    UIControl* m_unk74;                            // +0x74
    int   m_unk78;
    DWORD m_flags;                                 // +0x7C
    int   m_unk80;
    BYTE  m_unk84[0x0C];
    int   m_unk90;
    BYTE  m_unk94[0xC];
    int   m_unkA0;                                 // +0xA0: countdown, refilled from the clock in vslot43
    int   m_unkA4;
    HCURSOR m_cursor;                              // +0xA8: pushed on UIManager's cursor stack by vslot22/23
    UIColor m_color;                               // +0xAC
    bool  m_unkAF;
    bool  m_unkB0;
    bool  m_unkB1;
    BYTE  m_unkB2[6];
};                                                 // size 0xB8

#endif
