// ztaction.h - a family of small polymorphic "action" objects bound to an owner entity.
// Class names are placeholders (no RTTI in zoo.exe); slot 1 of every vtable returns a
// per-class id (0x01..0x86), see Src/misc/trivial_unowned.cpp.
//
//   ZTAction        vtable 0x6323C4, ctor 0x4139FD, dtor 0x41226C (BBT inlines both into every caller)
//   ZTActionBase    vtable 0x63244C, ctor 0x413A43 (32 leaf classes call it), dtor 0x43EBE3
//   leaf classes    ctor = base ctor + "owner is of my entity type" check, dtor = vptr resets
//                   (Notes/instances_actions.csv)
#ifndef ZTACTION_H
#define ZTACTION_H

struct ZTTypeInfo {
    virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3();
    virtual void v4(); virtual void v5(); virtual void v6();
    virtual bool isKindOf(const void* type);           // slot 7 (+0x1C)
};

struct ZTEntity {
    char m_unk00[0x128];
    ZTTypeInfo* m_type;                                 // +0x128
    char m_unk12C[0x15C - 0x12C];
    char m_sub[4];                                      // +0x15C
};

class ZTAction {
public:
    ZTAction(ZTEntity* owner, int arg);
    virtual ~ZTAction();                                // 0x41226C (out of line)
protected:
    ZTEntity* m_owner;                                  // +0x04
    void* m_ownerSub;                                   // +0x08 (&owner->m_sub)
    int m_arg;                                          // +0x0C
    bool m_done;                                        // +0x10
};

class ZTActionBase : public ZTAction {
public:
    ZTActionBase(ZTEntity* owner, int arg);
    virtual ~ZTActionBase();                            // 0x43EBE3 (out of line)
};

extern char g_entityType638700;                         // per-class static type objects
extern char g_entityType638760;

class ZTActionLeafA : public ZTAction {                 // reference copy 0x413ED7 (vtable 0x632F74)
public:
    ZTActionLeafA(ZTEntity* owner, int arg);
    virtual ~ZTActionLeafA();
protected:
    ZTEntity* m_target;                                 // +0x14
};

class ZTActionLeafB : public ZTActionBase {             // reference copy 0x42F860 (vtable 0x633C34)
public:
    ZTActionLeafB(ZTEntity* owner, int arg);
    virtual ~ZTActionLeafB();
protected:
    ZTEntity* m_target;                                 // +0x14
};

#endif
