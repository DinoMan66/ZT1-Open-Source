// uimanager.h - the global UI manager (g_uiManager, 0x638DE0). Only the members the
// reconstructed code uses are declared so far.
#ifndef UIMANAGER_H
#define UIMANAGER_H
#include <windows.h>

class UIControl;

class UIManager
{
public:
    /* 0x00 */ BYTE m_unk00[8];
    /* 0x08 */ UIControl* m_unk08;
    /* 0x0C */ UIControl* m_unk0C;
    /* 0x10 */ UIControl* m_focus;                 // control that vslot22/23 notify (name: guess)
    /* 0x14 */ UIControl* m_unk14;
    /* 0x18 */ UIControl* m_unk18;
    /* 0x1C */ BYTE m_unk1C[0x34];
    /* 0x50 */ HCURSOR m_unk50;                    // cursor stack state (name: offset only)
    /* 0x54 */ HCURSOR m_unk54;

    UIControl* find(int id);                       // 0x40157D
    void setFocus(UIControl* control);             // 0x44252D (name: MATCHING_NOTES 49)
    void f44316b(UIControl* control);              // 0x44316B
    void f443560(UIControl* control);              // 0x443560
    void f443dd0(int id);                          // 0x443DD0 (takes a control id; body not written yet)
    void f418f2f();                                // 0x418F2F
    void f418f43();                                // 0x418F43
    void f41ad6a(UIControl* control);              // 0x41AD6A
    void f4e0b8a(UIControl* control);              // 0x4E0B8A: drops `control` from the slots +0x08 / +0x10 / +0x14 / +0x18
    void f4d5bea();                                // 0x4D5BEA
    void setCursor(HCURSOR cursor, bool applyNow); // 0x418E81 (name: guess; a cursor of 0 pops the cursor stack)
};

extern UIManager g_uiManager;                      // 0x638DE0

#endif
