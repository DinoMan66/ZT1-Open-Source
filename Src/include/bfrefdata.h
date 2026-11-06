// bfrefdata.h - reference-counted data block and its smart handle (placeholder names, no RTTI).
//   BFRefDataBase::freeData 0x402EC7, BFMemCounter::sub 0x402F06 (BBT inlines it into freeData)
//   Per data type the game repeats the same non-template code (a macro or copies - VC6 would inline
//   template members): release (x29), handle set (x28, BBT inlines addRef), handle reset (x25).
//   BF_REFDATA(Name) declares one such pair; Notes/instances_refdata.csv lists the copies.
#ifndef BFREFDATA_H
#define BFREFDATA_H

struct BFMemCounter {
    int m_bytes;
    void sub(int n);
};
extern BFMemCounter g_memCounter;                       // 0x6380B0

class BFRefDataBase {
public:
    void freeData();
    int m_refs;                                         // +0x00
    int m_unk04;
    int m_unk08;
    char* m_data;                                       // +0x0C
    int m_size;                                         // +0x10
};

#define BF_REFDATA(Name)                                                    \
    class Name : public BFRefDataBase {                                     \
    public:                                                                 \
        void addRef();                                                      \
        void release();                                                     \
    };                                                                      \
    class Name##Handle {                                                    \
    public:                                                                 \
        void set(Name* p);                                                  \
        void reset();                                                       \
        Name* m_p;                                                          \
    };

#define BF_REFDATA_IMPL(Name)                                               \
    void Name::addRef() { ++m_refs; }                                       \
    void Name::release() { if (--m_refs == 0) freeData(); }                 \
    void Name##Handle::set(Name* p)                                         \
    {                                                                       \
        if (p == m_p)                                                       \
            return;                                                         \
        if (m_p)                                                            \
            m_p->release();                                                 \
        m_p = p;                                                            \
        if (p)                                                              \
            p->addRef();                                                    \
    }                                                                       \
    void Name##Handle::reset() { set(0); }

#endif
