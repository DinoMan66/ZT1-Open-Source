// gxvidman.h - GXVidMan: DirectDraw 7 setup, primary/back surfaces, flipping.
#ifndef GXVIDMAN_H
#define GXVIDMAN_H
#include "gxcanvas.h"

struct BFWindow                       // whatever owns the game window; only the HWND is used here
{
    bool isMinimized();               // 0x4D5FB5, out of line; BBT inlines it into its callers

    void* mUnknown0;
    HWND  mHwnd;                      // +0x04
    RECT  mRect;                      // +0x08: where the back buffer is blitted in windowed mode
};

class GXVidMan
{
public:
    bool initialize(BFWindow* window, GUID* driver);
    void shutdown();
    bool createDirectDraw(GUID* driver);
    void releaseDirectDraw();
    bool setupWindowed(bool setCooperativeLevel);
    bool createBltSurfaces();
    void releaseSurfaces();
    bool flip();
    bool createFlippingChain();

    bool useFlipping() { return mFullscreen && mFlipping && !mForceBlt; }

    BFWindow*            mWindow;         // +0x00
    bool                 mFullscreen;     // +0x04
    bool                 mFlipping;       // +0x05
    DWORD                mWidth;          // +0x08
    DWORD                mHeight;         // +0x0C
    DWORD                mUnknown10;      // +0x10
    bool                 mForceBlt;       // +0x14: blit even in fullscreen (name guessed)
    IDirectDraw7*        mDD;             // +0x18
    IDirectDrawSurface7* mPrimary;        // +0x1C
    IDirectDrawSurface7* mBack;           // +0x20
    GXCanvas             mPrimaryCanvas;  // +0x24
    GXCanvas             mBackCanvas;     // +0xBC
};

#endif
