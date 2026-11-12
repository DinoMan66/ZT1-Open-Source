// gxlle.h - GXLLE: a run-length-encoded sprite frame (original: C:\aqua\src\gx\gxlle*.cpp).
// Frame data: WORD rows (bit 15 = flag), WORD width, short yOffset, short xOffset, WORD ?, then per row
// a segment count and per segment: BYTE skip, BYTE count, count palette indices.
#ifndef GXLLE_H
#define GXLLE_H
#include "gxcanvas.h"

class GXPalette
{
public:
    BYTE  mUnknown00[0x28];
    BYTE* mEntries;          // +0x28: 256 x 4 bytes (B, G, R, x)
};

struct GXLLEFrame
{
    WORD  rows;              // & 0x7FFF
    WORD  width;
    short yOffset;
    short xOffset;
    WORD  unknown8;
    BYTE  data[1];           // +0x0A
};

class GXLLE
{
public:
    // gxlledither.cpp: draw blended 50% with a colour (B, G, R), mirrored, 32-bit target
    bool drawDitherMirror32(GXCanvas* canvas, GXPalette* palette, int x, int y, const BYTE* color);
    // gxlledither.cpp: the same for a 24-bit target (no alpha byte)
    bool drawDitherMirror24(GXCanvas* canvas, GXPalette* palette, int x, int y, const BYTE* color);

    // gxlle.cpp: draw unblended at zoom 1 to a 16-bit target, plain and mirrored
    bool draw16(GXCanvas* canvas, GXPalette* palette, int x, int y);
    bool drawMirror16(GXCanvas* canvas, GXPalette* palette, int x, int y);

    GXLLEFrame* mFrame;      // +0x00
};

#endif
