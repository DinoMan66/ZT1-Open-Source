// ztaction.cpp - constructors of the action family (see Src/include/ztaction.h).
#include "../include/ztaction.h"

ZTAction::ZTAction(ZTEntity* owner, int arg)
    : m_owner(owner)
{
    m_arg = arg;
    m_ownerSub = owner->m_sub;
    m_done = false;
}

ZTActionBase::ZTActionBase(ZTEntity* owner, int arg)
    : ZTAction(owner, arg)
{
}

// Leaf classes: remember the owner only if it is of the entity type the action is for.
ZTActionLeafA::ZTActionLeafA(ZTEntity* owner, int arg)
    : ZTAction(owner, arg)
{
    ZTEntity* owner_ = m_owner;
    m_target = (owner_ && owner_->m_type->isKindOf(&g_entityType638700)) ? owner_ : 0;
}

ZTActionLeafB::ZTActionLeafB(ZTEntity* owner, int arg)
    : ZTActionBase(owner, arg)
{
    ZTEntity* owner_ = m_owner;
    m_target = (owner_ && owner_->m_type->isKindOf(&g_entityType638760)) ? owner_ : 0;
}
