// ztgame.cpp - ZTGame, the part the UI handlers need.
#include "ztgame.h"

// 0x443FFA
bool ZTGame::contains(ZTEntity* entity)
{
    bool found = false;
    if (!entity)
        return found;
    for (_STL::vector<ZTEntity*>::iterator it = m_entities.begin(); it != m_entities.end(); ++it)
    {
        if (*it && *it == entity)
        {
            found = true;
            break;
        }
    }
    return found;
}
