// ztaimgr.cpp - ZTAIMgr (original unit not recorded).
#include <stdlib.h>
#include "ztaimgr.h"

// 0x4A9B8E  name: guess (the key "fMoveSlow"); true when the key names this movement speed
bool ZTAIMgr::isMoveSlow(const _STL::string& key)
{
    return key == "fMoveSlow";
}

// 0x4A9F0D  name: guess (the key "fMoveMedium")
bool ZTAIMgr::isMoveMedium(const _STL::string& key)
{
    return key == "fMoveMedium";
}

// 0x4AA02F  name: guess (the key "fMoveFast")
bool ZTAIMgr::isMoveFast(const _STL::string& key)
{
    return key == "fMoveFast";
}

// slot 7, 0x601E1C
void ZTAIMgr::vf7(int a, int b, int c, int d)
{
    vf6(a + 0x34, b + 0x34, c, d);
}

// slot 8, 0x601A50
int ZTAIMgr::vf8(int a)
{
    return m_unkDC;
}

// slot 9, 0x601A59
int ZTAIMgr::vf9(int a)
{
    return m_unkE0;
}

// slot 17, 0x60CAA8
bool ZTAIMgr::vf17(int a)
{
    return false;
}

// slot 13, 0x601E0A  (the key text is converted with the CRT's atoi, 0x405218)
int ZTAIMgr::vf13(const _STL::string& key, int b)
{
    return atoi(key.c_str());
}
