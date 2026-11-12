// ztgamemgr.cpp - ZTGameMgr (the original's file name is not recorded in zoo.exe).
#include <string>
#include "ztgamemgr.h"

// 0x41B55D [name guessed]: reads an integer setting, formatting the default as "%d" for the lookup
int getConfigInt(const std::string& section, const std::string& key, int defaultValue);

// 0x527EF1
ZTGameMgrBase::ZTGameMgrBase()
{
}

// merged into create() by BBT
ZTGameMgr::ZTGameMgr()
    : m_rules(0), m_unk1190(0), m_unk11A4(0)
{
    m_menuMusicMaxAttenuation = getConfigInt(std::string("UI"), std::string("menuMusicMaxAttenuation"), -1000);
}

// 0x527DC7
BFMgr* ZTGameMgr::create()
{
    return new ZTGameMgr;
}
