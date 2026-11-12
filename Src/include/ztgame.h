// ztgame.h - the game object g_638040 (the zoo being played), as far as the UI handlers use it.
#ifndef ZTGAME_H
#define ZTGAME_H

#include <windows.h>
#include <vector>
#include "ztentity.h"

// name: guess (the object the UI handlers ask whether an entity still belongs to the zoo)
struct ZTGame
{
    bool contains(ZTEntity* entity);            // 0x443FFA, BBT pastes it into the hint timers

    BYTE m_unk00[0x80];
    _STL::vector<ZTEntity*> m_entities;         // 0x80
};

extern ZTGame* g_638040;

#endif
