// gxlle.cpp - GXLLE drawing without blending, 16-bit target (original file name unknown: C:\aqua\src\gx\gxlle*.cpp).
// The renderer picks one variant per pixel format, zoom and mirror flag; these are zoom 1, 16 bits per pixel.
#include "gxlle.h"

// 0x4F47AA
// name: guess (medium) - the plain zoom-1 16-bit variant, by analogy with drawDitherMirror32
bool GXLLE::draw16(GXCanvas* canvas, GXPalette* palette, int x, int y)
{
    BYTE* entries = palette->mEntries;
    GXLLEFrame* frame = mFrame;
    int rows = frame->rows & 0x7FFF;
    int height = canvas->mDesc.dwHeight;
    int width = canvas->mDesc.dwWidth;
    BYTE* src = frame->data;
    y -= frame->yOffset;
    x -= frame->xOffset;
    if (y < height && rows + y > 0 && x < width && frame->width + x > 0)
    {
        // skip the rows above the top of the canvas
        for (; y < 0 && rows > 0; rows--)
        {
            for (int segments = *src++; segments != 0; segments--)
            {
                src++;
                int count = *src;
                src += count + 1;
            }
            y++;
        }
        WORD* line = (WORD*)((BYTE*)canvas->mDesc.lpSurface + canvas->mDesc.lPitch * y + x * 2);
        for (; y < height && rows > 0; rows--)
        {
            int px = x;
            WORD* dst = line;
            for (int segments = *src++; segments != 0; segments--)
            {
                int skip = *src++;
                px += skip;
                dst += skip;
                int count = *src++;
                BYTE* pixels = src;
                src += count;
                // clip the run against the left and right edges
                if (px < width)
                {
                    if (count < -px)
                    {
                        px += count;
                        dst += count;
                    }
                    else
                    {
                        if (px < 0)
                        {
                            count += px;
                            pixels -= px;
                            dst -= px;
                            px = 0;
                        }
                        if (px + count >= width)
                            count = width - px;
                        px += count;
                        while (count-- != 0)
                            *dst++ = *(WORD*)(entries + *pixels++ * 4);
                    }
                }
            }
            line = (WORD*)((BYTE*)line + canvas->mDesc.lPitch);
            y++;
        }
    }
    return true;
}

// 0x4F493B
// name: guess (medium) - the mirrored twin of draw16: x runs right to left from the frame's right edge
bool GXLLE::drawMirror16(GXCanvas* canvas, GXPalette* palette, int x, int y)
{
    GXLLEFrame* frame = mFrame;
    BYTE* entries = palette->mEntries;
    int height = canvas->mDesc.dwHeight;
    int width = canvas->mDesc.dwWidth;
    int rows = frame->rows & 0x7FFF;
    y -= frame->yOffset;
    x += frame->xOffset;
    BYTE* src = frame->data;
    if (y < height && rows + y > 0 && x >= 0 && x - frame->width < width)
    {
        // skip the rows above the top of the canvas
        for (; y < 0 && rows > 0; rows--)
        {
            for (int segments = *src++; segments != 0; segments--)
            {
                src++;
                int count = *src;
                src += count + 1;
            }
            y++;
        }
        WORD* line = (WORD*)((BYTE*)canvas->mDesc.lpSurface + canvas->mDesc.lPitch * y + x * 2);
        for (; y < height && rows > 0; rows--)
        {
            int px = x;
            WORD* dst = line;
            for (int segments = *src++; segments != 0; segments--)
            {
                int skip = *src++;
                px -= skip;
                dst -= skip;
                for (int count = *src++; count != 0; count--)
                {
                    BYTE index = *src++;
                    if (px >= 0 && px < width)
                        *dst = *(WORD*)(entries + index * 4);
                    dst--;
                    px--;
                }
            }
            line = (WORD*)((BYTE*)line + canvas->mDesc.lPitch);
            y++;
        }
    }
    return true;
}
