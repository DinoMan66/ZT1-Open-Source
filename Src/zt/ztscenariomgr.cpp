// ztscenariomgr.cpp - ZTScenarioMgr (original unit not recorded).
#include "ztscenariomgr.h"

// slot 3, 0x4C9BB2: back to the idle state; false when it was idle already
bool ZTScenarioMgr::vf3(int a)
{
    if (m_unk30 != 0)
    {
        m_unk30 = 0;
        return true;
    }
    return false;
}

// slot 4, 0x4B27E8: same as slot 3 without the argument
bool ZTScenarioMgr::vf4()
{
    if (m_unk30 != 0)
    {
        m_unk30 = 0;
        return true;
    }
    return false;
}

// slot 5, 0x4104CA
bool ZTScenarioMgr::vf5()
{
    return false;
}

// slot 11, 0x58E33E: goes from any non-idle state to state 4
bool ZTScenarioMgr::vf11()
{
    if (m_unk30 != 0)
    {
        m_unk30 = 4;
        return true;
    }
    return false;
}
