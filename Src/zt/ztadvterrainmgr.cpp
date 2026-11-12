// ztadvterrainmgr.cpp - ZTAdvTerrainMgr (original unit not recorded).
#include "ztadvterrainmgr.h"

bool g_638064;

// 0x40DCB4
void ZTAdvTerrainMgr::f40dcb4(int value)
{
    m_unk08 = value;
    g_638064 = value > 0;
}

// slot 1, 0x602DCF
bool ZTAdvTerrainMgr::vf1()
{
    f40dcb4(0);
    return true;
}
