// gximagebmp.cpp - GXImageBMP (original: C:\aqua\src\gx\gximagebmp.cpp).
#include "gximagebmp.h"

// 0x5234DA  name: string
bool GXImageBMP::attempt(const char* name)
{
    release();
    if (!mHandle.load(name))
    {
#line 65 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXImageBMP::attempt - Load failed: %s", name);
        return false;
    }
    // the file is read front to back: each header is taken at the cursor, which then moves past it
    BYTE* cursor = mHandle.mEntry ? (BYTE*)mHandle.mEntry->mData : 0;
    BITMAPFILEHEADER* fileHeader = (BITMAPFILEHEADER*)cursor;
    cursor += sizeof(BITMAPFILEHEADER);
    BITMAPINFOHEADER* info = (BITMAPINFOHEADER*)cursor;
    cursor += sizeof(BITMAPINFOHEADER);
    RGBQUAD* palette = (RGBQUAD*)cursor;
    if (fileHeader->bfType != 0x4D42)       // "BM"
    {
#line 76 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageBMP::attempt - Wrong type: %s", name);
        release();
        return false;
    }
    if (info->biSize != sizeof(BITMAPINFOHEADER))
    {
#line 86 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageBMP::attempt - Bad info header: %s", name);
        release();
        return false;
    }
    if (info->biCompression != BI_RGB)
    {
#line 93 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageBMP::attempt - Compressed data: %s", name);
        release();
        return false;
    }
    if (info->biPlanes != 1)
    {
#line 100 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageBMP::attempt - Multiplane data: %s", name);
        release();
        return false;
    }
    WORD bitCount = info->biBitCount;
    if (bitCount < 8 || bitCount > 32)
    {
#line 107 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXImageBMP - Bad bit count: %s", name);
        release();
        return false;
    }
    mInfo = info;
    mColorCount = info->biClrUsed;
    if (mColorCount == 0)
        mColorCount = 1 << info->biBitCount;
    if (info->biBitCount == 8)
    {
        mPalette = palette;
        palette += mColorCount;
    }
    else
        mPalette = 0;
    mPixels = palette;
#line 130 "C:\\aqua\\src\\gx\\gximagebmp.cpp"
    BFLog(BFLOG_ARGS(BFLOG_INFO), "GXImageBMP::attempt - %s (%d %d %d)", name, getWidth(), getHeight(), getBitCount());
    return true;
}

// 0x61F3B0  name: vtable (slot 4, the same check GXImageTGA / SNDSoundResourceWAV make)
int GXImageBMP::isValid()
{
    return mHandle.mEntry && mHandle.mEntry->mUnknown4 && mHandle.mEntry->mUnknown8 && mInfo && mPixels;
}

// 0x5235F1  name: body (the BITMAPINFOHEADER width; the attempt log prints width, height, bit count)
int GXImageBMP::getWidth()
{
    return mInfo ? mInfo->biWidth : 0;
}

// 0x5235E2
int GXImageBMP::getHeight()
{
    return mInfo ? mInfo->biHeight : 0;
}

// 0x5235D0
int GXImageBMP::getBitCount()
{
    return mInfo ? mInfo->biBitCount : 0;
}
