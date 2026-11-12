// ztgamemgr.h - ZTGameMgr, the game-rules manager (registered as "ZTGameMgr"). Size 0x11B0.
#ifndef ZTGAMEMGR_H
#define ZTGAMEMGR_H
#include <windows.h>
#include "bfmgr.h"

// [name invented] the object at ZTGameMgr+0x10; its constructor (0x4C2683, out of line) reads the
// escaped-animal and guest-limit settings (cEscapedAnimalChange, cEscapedAnimalTime, maxGuests).
class ZTGameRules
{
public:
    ZTGameRules(int unk);                          // 0x4C2683

    BYTE m_data[0x1180];
};

// [name invented] ZTGameMgr's direct base (vtable 0x6350D0, 6 slots, used by no other class). Its
// constructor is out of line (0x527EF1); BBT pasted the only call into ZTGameMgr::create.
class ZTGameMgrBase : public BFMgr                 // vtable 0x6350D0
{
public:
    ZTGameMgrBase();                               // 0x527EF1
    virtual ~ZTGameMgrBase();
    virtual void vf1();
    virtual void vf2();
    virtual void vf3();
    virtual void vf4();
    virtual void vf5();
};

class ZTGameMgr : public ZTGameMgrBase             // vtable 0x630B9C
{
public:
    ZTGameMgr();
    virtual ~ZTGameMgr();                          // 0x504DD8

    static const char s_className[];
    static bool s_registered;
    static BFMgr* create();

    BYTE        m_unk08[0x08];                     // +0x08
    ZTGameRules m_rules;                           // +0x10
    int         m_unk1190;                         // +0x1190
    BYTE        m_unk1194[0x10];
    int         m_unk11A4;                         // +0x11A4
    int         m_menuMusicMaxAttenuation;         // +0x11A8: [UI] menuMusicMaxAttenuation
    BYTE        m_unk11AC[0x04];
};

#endif
