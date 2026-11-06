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
    virtual ~UIElement();

    short m_unk04;
    short m_unk06;
    int   m_id;                                    // +0x08: unique id
    static int s_nextId;                           // 0x638D48
};

class UIControl : public UIElement                 // vtable 0x63203C
{
public:
    UIControl();                                   // 0x50F8E7
    virtual ~UIControl();
    void init();                                   // 0x4D2EDB (name unknown)

    // flag bits at +0x7C; body 0x4014AC, BBT inlined most of its 185 calls
    void setFlag(DWORD flag, bool on);
    bool flagBit(int bit) const { return (m_flags >> bit) & 1; }   // inline accessor (shr + test cl,1)

    // virtual slots the UI handlers call (names are guesses; slot = offset / 4)
    virtual void vslot01();
    virtual void vslot02();
    virtual void vslot03();
    virtual void vslot04();
    virtual void vslot05();
    virtual void vslot06();
    virtual void vslot07();
    virtual void vslot08();
    virtual void vslot09();
    virtual void vslot10();
    virtual void vslot11();
    virtual void vslot12();
    virtual void vslot13();
    virtual void vslot14();
    virtual void vslot15();
    virtual void vslot16();
    virtual void vslot17();
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
    virtual void vslot28();
    virtual void vslot29();
    virtual void vslot30();
    virtual void vslot31();
    virtual void vslot32();
    virtual void vslot33();
    virtual void vslot34();
    virtual void vslot35();
    virtual void vslot36();
    virtual void vslot37();
    virtual void vslot38();
    virtual void vslot39();
    virtual void vslot40();
    virtual void vslot41();
    virtual void vslot42();
    virtual void vslot43();
    virtual void vslot44();
    virtual void vslot45();
    virtual void vslot46();
    virtual void vslot47();
    virtual void vslot48();
    virtual void setText(_STL::string text, int a);   // slot 49 (+0xC4)
    virtual void vslot50(int id, int a);           // slot 50 (+0xC8): set a string/image by id?

    _STL::string m_name;                           // +0x0C
    _STL::string m_unk18;                          // +0x18
    _STL::string m_unk24;                          // +0x24
    BYTE  m_unk30[0x18];
    bool  m_unk48;                                 // +0x48
    BYTE  m_unk49[0x0F];
    _STL::vector<void*> m_unk58;                   // +0x58
    BYTE  m_unk64[0x10];
    UIControl* m_unk74;                            // +0x74
    int   m_unk78;
    DWORD m_flags;                                 // +0x7C
    int   m_unk80;
    BYTE  m_unk84[0x0C];
    int   m_unk90;
    BYTE  m_unk94[0x18];
    UIColor m_color;                               // +0xAC
    BYTE  m_unkAF[0x09];
};                                                 // size 0xB8

#endif
