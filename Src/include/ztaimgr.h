// ztaimgr.h - ZTAIMgr, the animal AI manager (class name from the registrar string; vtable 0x63536C, 18 slots).
// Only slots 10-12 are written so far; the others are unknown slots.
#ifndef ZTAIMGR_H
#define ZTAIMGR_H
#include <windows.h>
#include <string>

class ZTAIMgr
{
public:
    virtual ~ZTAIMgr();                                 // slot 0  0x503857
    virtual void vf1(); virtual void vf2(); virtual void vf3(); virtual void vf4();
    virtual void vf5();
    virtual void vf6(int a, int b, int c, int d);       // slot 6  0x43CEA4 (body not written)
    virtual void vf7(int a, int b, int c, int d);       // slot 7  0x601E1C: forwards to vf6 with a and b + 0x34
    virtual int vf8(int a);                             // slot 8  0x601A50: returns m_unkDC
    virtual int vf9(int a);                             // slot 9  0x601A59: returns m_unkE0
    virtual bool isMoveSlow(const _STL::string& key);   // slot 10 0x4A9B8E
    virtual bool isMoveMedium(const _STL::string& key); // slot 11 0x4A9F0D
    virtual bool isMoveFast(const _STL::string& key);   // slot 12 0x4AA02F
    virtual int vf13(const _STL::string& key, int b);   // slot 13 0x601E0A: atoi of the key
    virtual void vf14(); virtual void vf15(); virtual void vf16();
    virtual bool vf17(int a);                           // slot 17 0x60CAA8: returns false

    /* 0x04 */ BYTE m_unk04[0xD8];
    /* 0xDC */ int m_unkDC;
    /* 0xE0 */ int m_unkE0;
};

#endif
