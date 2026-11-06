// typedcall.cpp - "if the entity is a <type>, forward the call to it" (cluster 0x4224b0 x3). The type is tested
// twice: slot 6 then the isKindOf cast (slot 7). Names are placeholders Z_<address>.
struct ZTType6 {
    virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3(); virtual void v4(); virtual void v5();
    virtual bool is(const void* type);                 // slot 6 (+0x18)
    virtual bool isKindOf(const void* type);           // slot 7 (+0x1C)
};
struct ZTEnt6 { char m_unk00[0x128]; ZTType6* m_type; };

#define TYPED_CALL(name, type, cls, method)                                     \
    extern char type;                                                           \
    struct cls : ZTEnt6 { void method(int a); };                                \
    bool __stdcall name(ZTEnt6* e, int a)                                       \
    {                                                                           \
        if (e && e->m_type->is(&type)) {                                        \
            cls* p = e->m_type->isKindOf(&type) ? (cls*)e : 0;                  \
            p->method(a);                                                       \
        }                                                                       \
        return true;                                                            \
    }
TYPED_CALL(Z_4224B0, g_638700, ZTEnt700, m42201e)
TYPED_CALL(Z_4A941A, g_638780, ZTEnt780, m42201e)
TYPED_CALL(Z_58A953, g_638770, ZTEnt770, m58a929)
