// bfrefdata.cpp - see Src/include/bfrefdata.h
#include "../include/bfrefdata.h"

void BFMemCounter::sub(int n)
{
    m_bytes -= n;
}

void BFRefDataBase::freeData()
{
    if (m_data) {
        g_memCounter.sub(m_size);
        delete m_data;
        m_data = 0;
        m_size = 0;
    }
}

// reference copy of the per-type code
BF_REFDATA(BFRefProbe)
BF_REFDATA_IMPL(BFRefProbe)
