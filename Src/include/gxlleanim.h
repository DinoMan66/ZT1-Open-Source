// gxlleanim.h - GXLLEAnimSet: a set of low-level animations loaded from an .ani file
// (class name from the log strings "GXLLEAnimSet::attempt" / "GXLLEAnimSet::acquire").
// Original source: C:\aqua\src\gx\gxlleanim.cpp.
#ifndef GXLLEANIM_H
#define GXLLEANIM_H
#include "BFLog.h"

class GXLLEAnimSet
{
public:
    void acquire(const char* name);       // 0x4BDDBC: acquires the set and logs a failure
    bool f406a22(const char* name);       // 0x406A22 (name unknown): the unlogged acquire that ends in attempt (0x40B967)
};

#endif
