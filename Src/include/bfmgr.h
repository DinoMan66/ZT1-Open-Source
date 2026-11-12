// bfmgr.h - BFMgr, the base of the game's managers (registered through BFMgrFactory, BFRegistry.h).
// Its vtable 0x6355C0 has one slot; its inline constructor is stored by every manager constructor.
#ifndef BFMGR_H
#define BFMGR_H

class BFMgr                                        // vtable 0x6355C0
{
public:
    BFMgr() : m_unk04(false) {}
    virtual ~BFMgr();

    bool m_unk04;                                  // +0x04
};

#endif
