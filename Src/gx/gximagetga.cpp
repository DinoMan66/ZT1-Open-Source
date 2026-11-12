// gximagetga.cpp - GXImageTGA (original: C:\aqua\src\gx\gximagetga.cpp).
#include "gximagetga.h"

// 0x4B32A7  name: string
bool GXImageTGA::attempt(const char* name)
{
    release();
    if (!mHandle.load(name))
    {
#line 63 "C:\\aqua\\src\\gx\\gximagetga.cpp"
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXImageTGA::attempt - Load failed: %s", name);
        return false;
    }
    TGAHeader* header = mHandle.mEntry ? (TGAHeader*)mHandle.mEntry->mData : 0;
    if (header->mImageType != 2 && header->mImageType != 10)
    {
#line 73 "C:\\aqua\\src\\gx\\gximagetga.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageTGA::attempt - Wrong type: %s", name);
        release();
        return false;
    }
    WORD width = MAKEWORD(header->mWidthLow, header->mWidthHigh);
    WORD height = MAKEWORD(header->mHeightLow, header->mHeightHigh);
    if (width == 0 || height == 0)
    {
#line 79 "C:\\aqua\\src\\gx\\gximagetga.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageTGA::attempt - Zero image size: %s", name);
        release();
        return false;
    }
    WORD depth = header->mPixelDepth;
    if (depth < 24 || depth > 32)
    {
#line 86 "C:\\aqua\\src\\gx\\gximagetga.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageTGA::attempt - Invalid depth: %s %d", name, header->mPixelDepth);
        release();
        return false;
    }
    mHeader = header;
    // pixel data follows the header, the image id and the colour map
    int mapBytes = MAKEWORD(header->mMapLengthLow, header->mMapLengthHigh) * header->mMapEntryBits / 8;
    mPixels = (BYTE*)(header + 1) + header->mIdLength + mapBytes;
#line 97 "C:\\aqua\\src\\gx\\gximagetga.cpp"
    BFLog(BFLOG_ARGS(BFLOG_INFO), "GXImageTGA::attempt - %s (%d %d %d)", name, getWidth(), getHeight(), getDepth());
    return true;
}

// name: body (returns the header's width field; the attempt log prints width, height, depth)
int GXImageTGA::getWidth()                      // 0x4B33EC
{
    return MAKEWORD(mHeader->mWidthLow, mHeader->mWidthHigh);
}

int GXImageTGA::getHeight()                     // 0x4B33DE
{
    return MAKEWORD(mHeader->mHeightLow, mHeader->mHeightHigh);
}

int GXImageTGA::getDepth()                      // 0x4B33D3
{
    return mHeader->mPixelDepth;
}
