// ztadvterrainmgr.h - ZTAdvTerrainMgr (class name from the registrar string; vtable 0x630AD8, 5 slots).
// Slots 3 and 4 point at _purecall, so the class is abstract; only slot 1 is written so far.
#ifndef ZTADVTERRAINMGR_H
#define ZTADVTERRAINMGR_H
#include "bfmgr.h"

class ZTAdvTerrainMgr : public BFMgr
{
public:
    virtual ~ZTAdvTerrainMgr();                         // slot 0  0x602DB1
    virtual bool vf1();                                 // slot 1  0x602DCF
    virtual void vf2();                                 // slot 2  0x40100B
    virtual void vf3() = 0;                             // slot 3  _purecall
    virtual void vf4() = 0;                             // slot 4  _purecall

    void f40dcb4(int value);                            // 0x40DCB4

    /* 0x08 */ int m_unk08;
};

#endif
