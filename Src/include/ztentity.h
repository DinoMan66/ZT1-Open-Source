// ztentity.h - the game entity (animal, guest, building, ...) as far as the UI handlers use it.
#ifndef ZTENTITY_H
#define ZTENTITY_H

#include <windows.h>

// name: guess (the object an entity's m_type points to; the handlers ask it "is this entity a ...")
struct ZTTypeInfo
{
    virtual void vf0();
    virtual void vf1();
    virtual void vf2();
    virtual void vf3();
    virtual void vf4();
    virtual void vf5();
    virtual void vf6();
    virtual bool isKindOf(const void* type);    // slot 7, called by the info-panel handlers
};

// name: guess (the selected object of the screen returned by f410f84)
struct ZTEntity
{
    BYTE m_unk00[0x128];
    ZTTypeInfo* m_type;                         // 0x128

    void f5017ac();                             // 0x5017AC
};

#endif
