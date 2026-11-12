// bfapp.h - the game's application object (0x638148), created on first use by BFGetApp (0x4010C7).
// Only the window handle is used so far.
#ifndef BFAPP_H
#define BFAPP_H
#include <windows.h>

struct BFApp
{
    char pad[0x4C4];
    HWND m_hwnd;                                       // +0x4C4
};

BFApp* BFGetApp();                                     // 0x4010C7

#endif
