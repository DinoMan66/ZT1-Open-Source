// gxlledither.cpp - GXLLE drawing with a 50% colour blend (original: C:\aqua\src\gx\gxlledither.cpp).
// About 19 variants (pixel format, mirrored or not); zoom is a compile-time step of 1 here.
#include "gxlle.h"

// 0x472A25 - the 24-bit twin of drawDitherMirror32: same rows and segments, three colour bytes, no alpha.
bool GXLLE::drawDitherMirror24(GXCanvas* canvas, GXPalette* palette, int x, int y, const BYTE* color)
{
    BYTE* entries = palette->mEntries;
    GXLLEFrame* frame = mFrame;
    int bpp = canvas->mDesc.ddpfPixelFormat.dwRGBBitCount >> 3;
    int step = -bpp;
    BYTE* src = frame->data;
    int height = canvas->mDesc.dwHeight;
    int canvasWidth = canvas->mDesc.dwWidth;
    int rows = frame->rows & 0x7FFF;
    y -= frame->yOffset;
    x += frame->xOffset;

    if (y < height && rows + y >= 0 && x >= 0 && x - frame->width < canvasWidth)
    {
        bool locked = canvas->mLocked == 2;
        if (!locked)
        {
            canvas->lockWrite();
            if (canvas->mLocked != 2)
            {
#line 668 "C:\\aqua\\src\\gx\\gxlledither.cpp"
                BFLog(BFLOG_ARGS(BFLOG_ERROR), "GXLLE::draw - Lock.");
                return false;
            }
        }
        // skip the rows above the top of the canvas
        while (y + 1 <= 0)
        {
            if (--rows < 0)
                break;
            for (int segments = *src++; segments != 0; segments--)
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
            // rows above or below the canvas are skipped, but still advance line and y
            bool outside = y < 0 || y >= height;
            if (outside)
            {
                line += canvas->mDesc.lPitch;
                y++;
                for (int segments = *src++; segments != 0; segments--)
                {
                    src++;
                    int count = *src;
                    src += count + 1;
                }
                continue;
            }
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
                            *d = (*p >> 1) + (color[0] >> 1);
                        }
                        dst += step;
                        px--;
                    }
                    if (frac >= 1)
                        frac = 0;
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

// 0x4CAF3B
bool GXLLE::drawDitherMirror32(GXCanvas* canvas, GXPalette* palette, int x, int y, const BYTE* color)
{
    BYTE* entries = palette->mEntries;
    GXLLEFrame* frame = mFrame;
    int bpp = canvas->mDesc.ddpfPixelFormat.dwRGBBitCount >> 3;
    int step = -bpp;
    BYTE* src = frame->data;
    int height = canvas->mDesc.dwHeight;
    int canvasWidth = canvas->mDesc.dwWidth;
    int rows = frame->rows & 0x7FFF;
    y -= frame->yOffset;
    x += frame->xOffset;

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
        // skip the rows above the top of the canvas
        while (y + 1 <= 0)
        {
            if (--rows < 0)
                break;
            for (int segments = *src++; segments != 0; segments--)
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
            // rows above or below the canvas are skipped, but still advance line and y
            bool outside = y < 0 || y >= height;
            if (outside)
            {
                line += canvas->mDesc.lPitch;
                y++;
                for (int segments = *src++; segments != 0; segments--)
                {
                    src++;
                    int count = *src;
                    src += count + 1;
                }
                continue;
            }
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
            line += canvas->mDesc.lPitch;
            y++;
        }
        if (!locked)
            canvas->unlockSurface();
    }
    return true;
}
