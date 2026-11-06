// ztaction_dtor.cpp - destructors of the action family (see Src/include/ztaction.h).
// Leaf destructors (~74 copies) are only vptr resets; BBT inlines the base destructors into them.
#include "../include/ztaction.h"

ZTAction::~ZTAction() {}
ZTActionBase::~ZTActionBase() {}
ZTActionLeafA::~ZTActionLeafA() {}
ZTActionLeafB::~ZTActionLeafB() {}
