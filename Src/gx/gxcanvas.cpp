// gxcanvas.cpp - GXCanvas (original: C:\aqua\src\gx\gxcanvas.cpp).
// #line directives reproduce the original __LINE__ values and file name (__FILE__) passed to the logger.
#include <string.h>
#include "gxcanvas.h"

// 0x40710E
DWORD GXCanvas::getPixel(DWORD x, DWORD y)
{
    if (x >= mDesc.dwWidth || y >= mDesc.dwHeight)
    {
#line 143 "C:\\aqua\\src\\gx\\gxcanvas.cpp"
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXCanvas::getPixel - Invalid coord. (%d,%d)", x, y);
        return 0;
    }
    int wasLocked = mLocked;
    if (!wasLocked)
    {
        lockRead();
        if (mLocked != 1)
        {
#line 150
            BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXCanvas::getPixel - Failed to lock.");
            return 0;
        }
    }
    DWORD bytes = mDesc.ddpfPixelFormat.dwRGBBitCount >> 3;
    BYTE* p = (BYTE*)mDesc.lpSurface + y * mDesc.lPitch + bytes * x;
    DWORD pixel = 0;
    switch (bytes)
    {
    case 2: pixel = *(WORD*)p; break;
    case 3: memcpy(&pixel, p, 3); break;
    case 4: pixel = *(DWORD*)p; break;
    }
    if (!wasLocked)
        unlockSurface();
    return pixel;
}

// 0x4071CD
bool GXCanvas::setColorKey(DWORD x, DWORD y)
{
    DWORD key = getPixel(x, y);
    mDesc.ddckCKSrcBlt.dwColorSpaceLowValue = mDesc.ddckCKSrcBlt.dwColorSpaceHighValue = key;
    HRESULT hr = mSurface->SetColorKey(DDCKEY_SRCBLT, &mDesc.ddckCKSrcBlt);
    if (FAILED(hr))
    {
#line 222
        BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::setColorKey - SetColorKey.");
        return false;
    }
    mSurface->GetSurfaceDesc(&mDesc);
    return true;
}

// 0x4014C8
HDC GXCanvas::getDC()
{
    if (!mSurface)
    {
#line 375
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXCanvas::getDC - Null surface.");
        return NULL;
    }
    HDC hdc = NULL;
    HRESULT hr = mSurface->GetDC(&hdc);
    if (FAILED(hr))
#line 382
        BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::getDC - GetDC.");
    return hdc;
}

// 0x4014F5
bool GXCanvas::releaseDC(HDC hdc)
{
    if (!mSurface || !hdc)
    {
#line 391
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXCanvas::releaseDC - Null surface or DC.");
        return false;
    }
    HRESULT hr = mSurface->ReleaseDC(hdc);
    if (FAILED(hr))
    {
#line 397
        BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::releaseDC - ReleaseDC.");
        return false;
    }
    return true;
}
