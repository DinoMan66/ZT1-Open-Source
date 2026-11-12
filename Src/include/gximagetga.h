// gximagetga.h - GXImageTGA: an image loaded from a Targa (.tga) resource.
// Class name from the log strings "GXImageTGA::attempt ...". Original source: C:\aqua\src\gx\gximagetga.cpp.
// vtable at 0x6351EC: 2 attempt 0x4B32A7, 3 release 0x4072A3, 4 0x40733D.
#ifndef GXIMAGETGA_H
#define GXIMAGETGA_H
#include <windows.h>
#include "BFLog.h"
#include "sndsoundresource.h"   // BFResourceHandle / BFResourceEntry

struct TGAHeader                     // the 18-byte Targa file header, read byte by byte
{
    BYTE mIdLength;                  // +0x00
    BYTE mColorMapType;              // +0x01
    BYTE mImageType;                 // +0x02: 2 = uncompressed true-colour, 10 = RLE true-colour
    BYTE mMapStartLow;               // +0x03
    BYTE mMapStartHigh;              // +0x04
    BYTE mMapLengthLow;              // +0x05
    BYTE mMapLengthHigh;             // +0x06
    BYTE mMapEntryBits;              // +0x07
    BYTE mOriginXLow;                // +0x08
    BYTE mOriginXHigh;               // +0x09
    BYTE mOriginYLow;                // +0x0A
    BYTE mOriginYHigh;               // +0x0B
    BYTE mWidthLow;                  // +0x0C
    BYTE mWidthHigh;                 // +0x0D
    BYTE mHeightLow;                 // +0x0E
    BYTE mHeightHigh;                // +0x0F
    BYTE mPixelDepth;                // +0x10
    BYTE mDescriptor;                // +0x11
};

class GXImageTGA
{
public:
    virtual ~GXImageTGA();
    virtual void vf1();
    virtual bool attempt(const char* name);   // 0x4B32A7
    virtual void release();                   // 0x4072A3
    virtual int  vf4();                       // 0x40733D
    virtual int  getWidth();                  // 0x4B33EC
    virtual int  getHeight();                 // 0x4B33DE
    virtual int  getDepth();                  // 0x4B33D3: bits per pixel

    BFResourceHandle mHandle;                 // +0x04
    TGAHeader*       mHeader;                 // +0x08
    BYTE*            mPixels;                 // +0x0C
};

#endif
