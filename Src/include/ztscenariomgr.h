// ztscenariomgr.h - ZTScenarioMgr (class name from the registrar string; vtable 0x630DAC, 12 slots).
// Only a few small slots are written so far; the others are unknown slots.
#ifndef ZTSCENARIOMGR_H
#define ZTSCENARIOMGR_H
#include <windows.h>
#include "bfmgr.h"

class ZTScenarioMgr : public BFMgr
{
public:
    virtual ~ZTScenarioMgr();                           // slot 0  0x600019
    virtual void vf1();                                 // slot 1  0x58DE19
    virtual void vf2();                                 // slot 2  0x58EB71
    virtual bool vf3(int a);                            // slot 3  0x4C9BB2: leaves state 0 untouched, otherwise resets it
    virtual bool vf4();                                 // slot 4  0x4B27E8
    virtual bool vf5();                                 // slot 5  0x4104CA: returns false
    virtual void vf6(); virtual void vf7(); virtual void vf8(); virtual void vf9(); virtual void vf10();
    virtual bool vf11();                                // slot 11 0x58E33E

    /* 0x08 */ BYTE m_unk08[0x28];
    /* 0x30 */ int m_unk30;                             // state; 0 is the idle state
};

#endif
