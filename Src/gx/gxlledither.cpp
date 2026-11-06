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
#line 768 "C:\\aqua\\src\\gx\\gxlledither.cpp"
                BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXLLE::draw - Lock.");
                return false;
            }
        }
        while (y < 0)
        {
            if (--rows < 0)
                break;
            int segments = *src++;
            while (segments--)
            {
                src++;
                int count = *src;
                src += count + 1;
            }
            y++;
        }
        BYTE* line = (BYTE*)canvas->mDesc.lpSurface + canvas->mDesc.lPitch * y + bpp * x;
        while (y < height)
        {
            if (--rows < 0)
                break;
            if (y < 0 || y >= height)
            {
                int segments = *src++;
                while (segments--)
                {
                    src++;
                    int count = *src;
                    src += count + 1;
                }
            }
            else
            {
                int px = x;
                int frac = 0;
                BYTE* dst = line;
                int segments = *src++;
                while (segments--)
                {
                    int skip = *src++;
                    while (skip--)
                    {
                        if (frac++ == 0)
                        {
                            dst += step;
                            px--;
                        }
                        if (frac >= 1)
                            frac = 0;
                    }
                    int count = *src++;
                    while (count--)
                    {
                        BYTE index = *src++;
                        if (frac++ == 0)
                        {
                            if (px >= 0 && px < canvasWidth)
                            {
                                BYTE* p = entries + index * 4;
                                dst[0] = (color[2] >> 1) + (p[0] >> 1);
                                dst[1] = (color[1] >> 1) + (p[1] >> 1);
                                dst[2] = (p[2] >> 1) + (color[0] >> 1);
                                dst[3] = 0xFF;
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
