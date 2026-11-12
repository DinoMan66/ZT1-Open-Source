// gximagebmp.h - GXImageBMP: an image loaded from a Windows bitmap (.bmp) resource.
// Class name from the log strings "GXImageBMP::attempt ...". Original source: C:\aqua\src\gx\gximagebmp.cpp.
// vtable at 0x63585C: 0 dtor 0x523B64, 2 attempt 0x5234DA, 3 release 0x4C6714, 4 isValid 0x61F3B0,
// 5 getWidth 0x5235F1, 6 getHeight 0x5235E2, 7 getBitCount 0x5235D0.
#ifndef GXIMAGEBMP_H
#define GXIMAGEBMP_H
#include <windows.h>
#include "BFLog.h"
#include "sndsoundresource.h"   // BFResourceHandle / BFResourceEntry

class GXImageBMP
{
public:
    virtual ~GXImageBMP();
    virtual void vf1();
    virtual bool attempt(const char* name);   // 0x5234DA
    virtual void release();                   // 0x4C6714
    virtual int  isValid();                   // 0x61F3B0
    virtual int  getWidth();                  // 0x5235F1
    virtual int  getHeight();                 // 0x5235E2
    virtual int  getBitCount();               // 0x5235D0

    BFResourceHandle  mHandle;                // +0x04
    int               mColorCount;            // +0x08: palette entries
    BITMAPINFOHEADER* mInfo;                  // +0x0C
    RGBQUAD*          mPalette;               // +0x10: only for 8-bit bitmaps
    void*             mPixels;                // +0x14
};

#endif
