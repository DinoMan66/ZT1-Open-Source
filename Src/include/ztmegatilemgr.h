// ztmegatilemgr.h - ZTMegatileMgr (class name from the registrar string s_className 0x6415F8;
// vtable 0x6355C4, one slot (the destructor)). Derived from BFMgr.
#ifndef ZTMEGATILEMGR_H
#define ZTMEGATILEMGR_H
#include <windows.h>
#include "bfmgr.h"

class ZTMegatileMgr : public BFMgr
{
public:
    ZTMegatileMgr()
    {
        m_unk18 = 0;
        m_unk1C = 0;
        m_unk20 = 0;
    }
    virtual ~ZTMegatileMgr();                           // slot 0

    static BFMgr* create();                             // 0x463E1E

    /* 0x08 */ BYTE m_unk08[0x10];
    /* 0x18 */ int m_unk18;
    /* 0x1C */ int m_unk1C;
    /* 0x20 */ int m_unk20;
};

#endif
