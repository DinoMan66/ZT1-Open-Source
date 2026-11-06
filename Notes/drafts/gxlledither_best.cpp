// DRAFT (round 047 VarD, best so far: frame 0x24 right, clip loop right; register assignment still differs:
// original keeps canvas in ebx and spills y/x to their argument slots). Declaration order, local copies,
// unsigned counters and loop forms (round 048) do not change VC6's choice. Copy into Src/gx when it matches.
// gxlledither.cpp - GXLLE drawing with a 50% colour blend (original: C:\aqua\src\gx\gxlledither.cpp).
// About 19 variants (pixel format, mirrored or not); zoom is a compile-time step of 1 here.
#include "gxlle.h"

// 0x4CAF3B
bool GXLLE::drawDitherMirror32(GXCanvas* canvas, GXPalette* palette, int x, int y, const BYTE* color)
{
    BYTE* entries = palette->mEntries;
    GXLLEFrame* frame = mFrame;
    int canvasWidth = canvas->mDesc.dwWidth;
    int rows = frame->rows & 0x7FFF;
    y -= frame->yOffset;
    int bpp = canvas->mDesc.ddpfPixelFormat.dwRGBBitCount >> 3;
    x += frame->xOffset;
    int step = -bpp;
    int height = canvas->mDesc.dwHeight;
    BYTE* src = frame->data;

    if (y < height && rows + y >= 0 && x >= 0 && x - frame->width < canvasWidth)
    {
        bool locked = canvas->mLocked == 2;
        if (!locked)
        {
            canvas->lockWrite();
            if (canvas->mLocked != 2)
            {
#line 768
                BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXLLE::draw - Lock.");
                return false;
            }
        }
        while (y + 1 <= 0)
        {
            if (--rows < 0)
                break;
            for (int n = *src++; n != 0; n--)
            {
                src++;
                src += *src + 1;
            }
            y++;
        }
        BYTE* line = canvas->mDesc.lPitch * y + bpp * x + (BYTE*)canvas->mDesc.lpSurface;
        while (y < height)
        {
            if (--rows < 0)
                break;
            if (y < 0 || y >= height)
            {
                for (int n = *src++; n != 0; n--)
                {
                    src++;
                    src += *src + 1;
                }
            }
            else
            {
                int px = x;
                int frac = 0;
                BYTE* dst = line;
                for (int segments = *src++; segments != 0; segments--)
                {
                    for (int skip = *src++; skip != 0; skip--)
                    {
                        if (frac++ == 0)
                        {
                            dst += step;
                            px--;
                        }
                        if (frac >= 1)
                            frac = 0;
                    }
                    for (int count = *src++; count != 0; count--)
                    {
                        BYTE index = *src++;
                        if (frac++ == 0)
                        {
                            if (px >= 0 && px < canvasWidth)
                            {
                                BYTE* p = entries + index * 4;
                                BYTE* d = dst;
                                *d++ = (color[2] >> 1) + (*p++ >> 1);
                                *d++ = (color[1] >> 1) + (*p++ >> 1);
                                *d++ = (*p >> 1) + (color[0] >> 1);
                                *d = 0xFF;
                            }
                            dst += step;
                            px--;
                        }
                        if (frac >= 1)
                            frac = 0;
                    }
                }
            }
            line += canvas->mDesc.lPitch;
            y++;
        }
        if (!locked)
            canvas->unlockSurface();
    }
    return true;
}
