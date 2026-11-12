// gxlleanim.cpp - GXLLEAnimSet (original: C:\aqua\src\gx\gxlleanim.cpp).
#include "gxlleanim.h"

// 0x4BDDBC
// name: string ("GXLLEAnimSet::acquire - Failed to acquire <%s>")
void GXLLEAnimSet::acquire(const char* name)
{
    if (!f406a22(name))
    {
#line 463 "C:\\aqua\\src\\gx\\gxlleanim.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXLLEAnimSet::acquire - Failed to acquire <%s>", name);
    }
}
