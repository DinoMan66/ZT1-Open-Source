// gxvidman.cpp - GXVidMan (original: C:\aqua\src\gx\gxvidman.cpp).
#include <string.h>
#include "gxvidman.h"

// 0x533DB5
bool GXVidMan::initialize(BFWindow* window, GUID* driver)
{
#line 26 "C:\\aqua\\src\\gx\\gxvidman.cpp"
    BFLog(BFLOG_ARGS(BFLOG_TRACE), "GXVidMan::initialize - Initializing.");
    if (!window || !window->mHwnd || !IsWindow(window->mHwnd))
    {
#line 30
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXVidMan::initialize - Null window handle.");
        return false;
    }
    if (mDD)
    {
#line 36
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXVidMan::initialize - Already started.");
        return false;
    }
    if (!createDirectDraw(driver))
        return false;
    mWindow = window;
#line 48
    BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::initialize - Initialization successful.");
    return true;
}

// 0x57DF69
void GXVidMan::shutdown()
{
#line 146
    BFLog(BFLOG_ARGS(BFLOG_TRACE), "GXVidMan::shutdown - Shutting down.");
    releaseSurfaces();
    releaseDirectDraw();
#line 151
    BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::shutdown - Shutdown successful.");
}

// 0x4D5FB5  BFWindow::isMinimized - a real out-of-line function in the original; BBT inlined the call
// into flip (which is why mWindow sits in ecx there: it was the `this` of a call). Its proper home is the
// BFWindow source file once that class is written; kept here so compare.py can expand the call.
bool BFWindow::isMinimized()
{
    return IsIconic(mHwnd) != 0;
}

// 0x4013BF
bool GXVidMan::flip()
{
    RECT* dest = NULL;
    HRESULT hr;
    if (!mPrimary || !mWindow)
    {
#line 171
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXVidMan::flip - No primary surface.");
        shutdown();
        return false;
    }
    if (useFlipping())
        hr = mPrimary->Flip(NULL, DDFLIP_WAIT);
    else
    {
        dest = &mWindow->mRect;
        hr = mPrimary->Blt(dest, mBack, NULL, DDBLT_WAIT, NULL);
    }
    if (SUCCEEDED(hr))
    {
#line 186
        BFLog(BFLOG_ARGS(BFLOG_TRACE), "GXVidMan::flip - Flipped.");
        return true;
    }
    if (mWindow->isMinimized())
    {
#line 190
        BFLog(BFLOG_ARGS(BFLOG_INFO), "GXVidMan::flip - Window minimized, skipping.");
        return true;
    }
    if (hr != DDERR_SURFACELOST)
    {
#line 194
        BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::flip - Flip failed.");
        return false;
    }
    hr = mDD->RestoreAllSurfaces();
#line 201
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::flip - Restore all surfaces.");
    if (useFlipping())
        hr = mPrimary->Flip(NULL, DDFLIP_WAIT);
    else
        hr = mPrimary->Blt(dest, mBack, NULL, DDBLT_WAIT, NULL);
#line 212
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::flip - Second flip.");
    return SUCCEEDED(hr);
}

// 0x533D0A
bool GXVidMan::createDirectDraw(GUID* driver)
{
    if (!mDD)
    {
        HRESULT hr = CoCreateInstance(CLSID_DirectDraw7, NULL, CLSCTX_ALL, IID_IDirectDraw7, (void**)&mDD);
#line 237
        BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createDirectDraw - CoCreateInstance");
        if (FAILED(hr))
            return false;
        hr = mDD->Initialize(driver);
#line 243
        BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createDirectDraw - Initialize");
        if (FAILED(hr))
        {
            mDD->Release();
            mDD = NULL;
            return false;
        }
#line 251
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::createDirectDraw - Created.");
    }
    return true;
}

// 0x57E01E
void GXVidMan::releaseDirectDraw()
{
    if (mDD)
    {
        mDD->Release();
        mDD = NULL;
#line 263
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::releaseDirectDraw - Released.");
    }
}

// 0x52F1D0
bool GXVidMan::setupWindowed(bool setCooperativeLevel)
{
    mFullscreen = false;
    mFlipping = false;
    if (setCooperativeLevel)
    {
        HRESULT hr = mDD->SetCooperativeLevel(mWindow->mHwnd, DDSCL_NORMAL);
#line 340
        BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::setupWindowed - SetCooperativeLevel");
        if (FAILED(hr))
            return false;
    }
    if (createBltSurfaces())
    {
#line 347
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::setupWindowed - Surfaces created.");
        return true;
    }
    return false;
}

// 0x4D6AE1
bool GXVidMan::createFlippingChain()
{
    IDirectDrawClipper* clipper;
    DDSURFACEDESC2 desc;
    memset(&desc, 0, sizeof(desc));
    desc.dwSize = sizeof(desc);
    desc.dwFlags = DDSD_CAPS | DDSD_BACKBUFFERCOUNT;
    desc.ddsCaps.dwCaps |= DDSCAPS_PRIMARYSURFACE | DDSCAPS_FLIP | DDSCAPS_COMPLEX;
    desc.dwBackBufferCount = 1;
    HRESULT hr = mDD->CreateSurface(&desc, &mPrimary, NULL);
#line 369
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createFlippingChain - CreateSurface");
    if (FAILED(hr))
        return false;

    desc.ddsCaps.dwCaps = DDSCAPS_BACKBUFFER;
    hr = mPrimary->GetAttachedSurface(&desc.ddsCaps, &mBack);
#line 377
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createFlippingChain - GetAttachedSurface");
    if (FAILED(hr))
        return false;

    clipper = NULL;
    hr = mDD->CreateClipper(0, &clipper, NULL);
#line 385
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createFlippingChain - CreateClipper");
    if (FAILED(hr))
        return false;

    hr = clipper->SetHWnd(0, mWindow->mHwnd);
#line 392
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createFlippingChain - SetHwnd");
    if (FAILED(hr))
        return false;

    hr = mPrimary->SetClipper(clipper);
#line 399
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createFlippingChain - SetClipper");
    if (FAILED(hr))
        return false;

    clipper->Release();
    return true;
}

// 0x52F2A6
bool GXVidMan::createBltSurfaces()
{
    IDirectDrawClipper* clipper;
    DDSURFACEDESC2 desc;
    memset(&desc, 0, sizeof(desc));
    desc.dwSize = sizeof(desc);
    desc.dwFlags = DDSD_CAPS;
    desc.ddsCaps.dwCaps = DDSCAPS_PRIMARYSURFACE;
    HRESULT hr = mDD->CreateSurface(&desc, &mPrimary, NULL);
#line 423
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createBltSurfaces - CreateSurface [primary]");
    if (FAILED(hr))
        return false;

    desc.dwWidth = mWidth;
    desc.dwHeight = mHeight;
    desc.dwFlags |= DDSD_HEIGHT | DDSD_WIDTH;
    desc.ddsCaps.dwCaps = DDSCAPS_OFFSCREENPLAIN;
    hr = mDD->CreateSurface(&desc, &mBack, NULL);
#line 436
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createBltSurfaces - CreateSurface [backbuf]");
    if (FAILED(hr))
        return false;

    clipper = NULL;
    hr = mDD->CreateClipper(0, &clipper, NULL);
#line 444
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createBltSurfaces - CreateClipper");
    if (FAILED(hr))
        return false;

    hr = clipper->SetHWnd(0, mWindow->mHwnd);
#line 451
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createBltSurfaces - SetHwnd");
    if (FAILED(hr))
        return false;

    hr = mPrimary->SetClipper(clipper);
#line 458
    BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::createBltSurfaces - SetClipper");
    if (FAILED(hr))
        return false;

    clipper->Release();
    return true;
}

// 0x4D67A2
void GXVidMan::releaseSurfaces()
{
    if (mDD)
    {
        if (mFullscreen)
        {
            HRESULT hr = mDD->RestoreDisplayMode();
#line 480
            BFLogHR(BFLOG_HR_ARGS(hr), "GXVidMan::releaseSurfaces - RestoreDisplayMode");
        }
        if (mBack)
        {
            mBackCanvas.releaseSurface();
            while (mBack->Release() > 0)
                ;
#line 487
            BFLog(BFLOG_ARGS(BFLOG_INFO), "GXVidMan::releaseSurfaces - Backbuf released.");
        }
        if (mPrimary)
        {
            mPrimaryCanvas.releaseSurface();
            while (mPrimary->Release() > 0)
                ;
#line 494
            BFLog(BFLOG_ARGS(BFLOG_NOTE), "GXVidMan::releaseSurfaces - Primary released.");
        }
        mPrimary = NULL;
        mBack = NULL;
    }
}
