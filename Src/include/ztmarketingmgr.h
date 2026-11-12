// ztmarketingmgr.h - ZTMarketingMgr (class name from the registrar string s_className 0x643E04;
// vtable 0x635110, 4 slots, none written yet). Derived from BFMgr; the factory create() stores the vtable
// pointer after the members, like the other registered managers.
#ifndef ZTMARKETINGMGR_H
#define ZTMARKETINGMGR_H
#include "bfmgr.h"

class ZTMarketingMgr : public BFMgr
{
public:
    ZTMarketingMgr()
    {
        m_unk08 = 0;
        m_unk0C = 0;
    }
    virtual ~ZTMarketingMgr();                          // slot 0
    virtual void vf1();
    virtual void vf2();
    virtual void vf3();

    static BFMgr* create();                             // 0x5257E7

    /* 0x08 */ int m_unk08;
    /* 0x0C */ int m_unk0C;
};

#endif
