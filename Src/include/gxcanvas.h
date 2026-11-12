// gxcanvas.h - GXCanvas: a DirectDraw 7 surface plus its cached description.
// Original header: ..\inc\gxcanvas.h (line numbers below are the original's, via #line).
#ifndef GXCANVAS_H
#define GXCANVAS_H
#include "bfddraw.h"
#include "BFLog.h"

class GXCanvas
{
public:
    ~GXCanvas();                                   // 0x40511C
    GXCanvas& operator=(const GXCanvas& other);    // 0x41BC05: takes over the other canvas's surface
    DWORD getPixel(DWORD x, DWORD y);
    bool  setColorKey(DWORD x, DWORD y);
    HDC   getDC();
    bool  releaseDC(HDC hdc);

    void lockRead()
    {
        if (mSurface && !mLocked)
        {
            HRESULT hr = mSurface->Lock(NULL, &mDesc, DDLOCK_WAIT | DDLOCK_READONLY | DDLOCK_NOSYSLOCK, NULL);
            if (FAILED(hr))
#line 125 "..\\inc\\gxcanvas.h"
                BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::lockRead - Lock.");
            else
                mLocked = 1;
        }
    }

    // mLocked: 0 = unlocked, 1 = locked for reading, 2 = locked for writing
    void lockWrite()
    {
        if (mSurface && !mLocked)
        {
            HRESULT hr = mSurface->Lock(NULL, &mDesc, DDLOCK_WAIT | DDLOCK_WRITEONLY | DDLOCK_NOSYSLOCK, NULL);
            if (FAILED(hr))
#line 139
                BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::lockWrite - Lock.");
            else
                mLocked = 2;
            if (!mDesc.lpSurface)
#line 144
                BFLog(BFLOG_ARGS(BFLOG_ERROR), "mDesc.lpSurface = 0");
        }
    }

    void unlockSurface()
    {
        if (mSurface && mLocked)
        {
            HRESULT hr = mSurface->Unlock(NULL);
            if (FAILED(hr))
#line 157
                BFLogHR(BFLOG_HR_ARGS(hr), "GXCanvas::unlockSurface - Unlock.");
            else
                mLocked = 0;
        }
    }

    // releases the surface pointer (inlined into GXVidMan::releaseSurfaces)
    void releaseSurface()
    {
        if (mSurface)
        {
            mSurface->Release();
            mSurface = NULL;
        }
    }

    int                  mLocked;      // +0x00: 1 while the surface is locked
    DDSURFACEDESC2       mDesc;        // +0x04
    IDirectDrawSurface7* mSurface;     // +0x80
    DWORD                mUnknown84[5]; // +0x84 .. +0x97 (size 0x98, from GXVidMan's layout)
};

#endif
