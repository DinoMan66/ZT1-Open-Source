// bfddraw.h - the DirectDraw 7 declarations zoo.exe uses (layouts and vtable order as in the
// DirectX 7 ddraw.h). VC6's own ddraw.h predates IDirectDrawSurface7.
#ifndef BFDDRAW_H
#define BFDDRAW_H
#include <windows.h>
#include <objbase.h>

struct DDCOLORKEY { DWORD dwColorSpaceLowValue; DWORD dwColorSpaceHighValue; };
struct DDPIXELFORMAT
{
    DWORD dwSize, dwFlags, dwFourCC;
    union { DWORD dwRGBBitCount; DWORD dwYUVBitCount; DWORD dwZBufferBitDepth; DWORD dwAlphaBitDepth; };
    union { DWORD dwRBitMask; DWORD dwYBitMask; };
    union { DWORD dwGBitMask; DWORD dwUBitMask; };
    union { DWORD dwBBitMask; DWORD dwVBitMask; };
    union { DWORD dwRGBAlphaBitMask; DWORD dwYUVAlphaBitMask; };
};
struct DDSCAPS2 { DWORD dwCaps, dwCaps2, dwCaps3, dwCaps4; };
struct DDSURFACEDESC2                       // 0x7C bytes
{
    DWORD dwSize, dwFlags, dwHeight, dwWidth;
    union { LONG lPitch; DWORD dwLinearSize; };
    union { DWORD dwBackBufferCount; DWORD dwDepth; };
    union { DWORD dwMipMapCount; DWORD dwRefreshRate; };
    DWORD dwAlphaBitDepth, dwReserved;
    LPVOID lpSurface;
    DDCOLORKEY ddckCKDestOverlay, ddckCKDestBlt, ddckCKSrcOverlay, ddckCKSrcBlt;
    DDPIXELFORMAT ddpfPixelFormat;
    DDSCAPS2 ddsCaps;
    DWORD dwTextureStage;
};

#define DDCKEY_SRCBLT       0x00000008
#define DDLOCK_WAIT         0x00000001
#define DDLOCK_READONLY     0x00000010
#define DDLOCK_WRITEONLY    0x00000020
#define DDLOCK_NOSYSLOCK    0x00000800

struct IDirectDrawSurface7 : public IUnknown
{
    STDMETHOD(AddAttachedSurface)(IDirectDrawSurface7*) PURE;
    STDMETHOD(AddOverlayDirtyRect)(LPRECT) PURE;
    STDMETHOD(Blt)(LPRECT, IDirectDrawSurface7*, LPRECT, DWORD, void*) PURE;                // 0x14
    STDMETHOD(BltBatch)(void*, DWORD, DWORD) PURE;
    STDMETHOD(BltFast)(DWORD, DWORD, IDirectDrawSurface7*, LPRECT, DWORD) PURE;
    STDMETHOD(DeleteAttachedSurface)(DWORD, IDirectDrawSurface7*) PURE;
    STDMETHOD(EnumAttachedSurfaces)(LPVOID, void*) PURE;
    STDMETHOD(EnumOverlayZOrders)(DWORD, LPVOID, void*) PURE;
    STDMETHOD(Flip)(IDirectDrawSurface7*, DWORD) PURE;
    STDMETHOD(GetAttachedSurface)(DDSCAPS2*, IDirectDrawSurface7**) PURE;
    STDMETHOD(GetBltStatus)(DWORD) PURE;
    STDMETHOD(GetCaps)(DDSCAPS2*) PURE;
    STDMETHOD(GetClipper)(void**) PURE;
    STDMETHOD(GetColorKey)(DWORD, DDCOLORKEY*) PURE;
    STDMETHOD(GetDC)(HDC*) PURE;                                   // 0x44
    STDMETHOD(GetFlipStatus)(DWORD) PURE;
    STDMETHOD(GetOverlayPosition)(LPLONG, LPLONG) PURE;
    STDMETHOD(GetPalette)(void**) PURE;
    STDMETHOD(GetPixelFormat)(DDPIXELFORMAT*) PURE;
    STDMETHOD(GetSurfaceDesc)(DDSURFACEDESC2*) PURE;               // 0x58
    STDMETHOD(Initialize)(void*, DDSURFACEDESC2*) PURE;
    STDMETHOD(IsLost)() PURE;
    STDMETHOD(Lock)(LPRECT, DDSURFACEDESC2*, DWORD, HANDLE) PURE;  // 0x64
    STDMETHOD(ReleaseDC)(HDC) PURE;                                // 0x68
    STDMETHOD(Restore)() PURE;
    STDMETHOD(SetClipper)(struct IDirectDrawClipper*) PURE;                         // 0x70
    STDMETHOD(SetColorKey)(DWORD, DDCOLORKEY*) PURE;               // 0x74
    STDMETHOD(SetOverlayPosition)(LONG, LONG) PURE;
    STDMETHOD(SetPalette)(void*) PURE;
    STDMETHOD(Unlock)(LPRECT) PURE;                                // 0x80
    STDMETHOD(UpdateOverlay)(LPRECT, IDirectDrawSurface7*, LPRECT, DWORD, void*) PURE;
    STDMETHOD(UpdateOverlayDisplay)(DWORD) PURE;
    STDMETHOD(UpdateOverlayZOrder)(DWORD, IDirectDrawSurface7*) PURE;
    STDMETHOD(GetDDInterface)(LPVOID*) PURE;
    STDMETHOD(PageLock)(DWORD) PURE;
    STDMETHOD(PageUnlock)(DWORD) PURE;
    STDMETHOD(SetSurfaceDesc)(DDSURFACEDESC2*, DWORD) PURE;
    STDMETHOD(SetPrivateData)(REFGUID, LPVOID, DWORD, DWORD) PURE;
    STDMETHOD(GetPrivateData)(REFGUID, LPVOID, LPDWORD) PURE;
    STDMETHOD(FreePrivateData)(REFGUID) PURE;
    STDMETHOD(GetUniquenessValue)(LPDWORD) PURE;
    STDMETHOD(ChangeUniquenessValue)() PURE;
    STDMETHOD(SetPriority)(DWORD) PURE;
    STDMETHOD(GetPriority)(LPDWORD) PURE;
    STDMETHOD(SetLOD)(DWORD) PURE;
    STDMETHOD(GetLOD)(LPDWORD) PURE;
};

#define DDSD_CAPS               0x00000001
#define DDSD_HEIGHT             0x00000002
#define DDSD_WIDTH              0x00000004
#define DDSD_BACKBUFFERCOUNT    0x00000020
#define DDSCAPS_BACKBUFFER      0x00000004
#define DDSCAPS_COMPLEX         0x00000008
#define DDSCAPS_FLIP            0x00000010
#define DDSCAPS_OFFSCREENPLAIN  0x00000040
#define DDSCAPS_PRIMARYSURFACE  0x00000200
#define DDSCL_NORMAL            0x00000008
#define DDFLIP_WAIT             0x00000001
#define DDBLT_WAIT              0x01000000
#define DDERR_SURFACELOST       ((HRESULT)0x887601C2)

struct IDirectDrawClipper : public IUnknown
{
    STDMETHOD(GetClipList)(LPRECT, LPVOID, LPDWORD) PURE;
    STDMETHOD(GetHWnd)(HWND*) PURE;
    STDMETHOD(Initialize)(LPVOID, DWORD) PURE;
    STDMETHOD(IsClipListChanged)(BOOL*) PURE;
    STDMETHOD(SetClipList)(LPVOID, DWORD) PURE;
    STDMETHOD(SetHWnd)(DWORD, HWND) PURE;                          // 0x20
};

struct IDirectDraw7 : public IUnknown
{
    STDMETHOD(Compact)() PURE;
    STDMETHOD(CreateClipper)(DWORD, IDirectDrawClipper**, IUnknown*) PURE;          // 0x10
    STDMETHOD(CreatePalette)(DWORD, LPPALETTEENTRY, void**, IUnknown*) PURE;
    STDMETHOD(CreateSurface)(DDSURFACEDESC2*, IDirectDrawSurface7**, IUnknown*) PURE; // 0x18
    STDMETHOD(DuplicateSurface)(IDirectDrawSurface7*, IDirectDrawSurface7**) PURE;
    STDMETHOD(EnumDisplayModes)(DWORD, DDSURFACEDESC2*, LPVOID, void*) PURE;
    STDMETHOD(EnumSurfaces)(DWORD, DDSURFACEDESC2*, LPVOID, void*) PURE;
    STDMETHOD(FlipToGDISurface)() PURE;
    STDMETHOD(GetCaps)(void*, void*) PURE;
    STDMETHOD(GetDisplayMode)(DDSURFACEDESC2*) PURE;
    STDMETHOD(GetFourCCCodes)(LPDWORD, LPDWORD) PURE;
    STDMETHOD(GetGDISurface)(IDirectDrawSurface7**) PURE;
    STDMETHOD(GetMonitorFrequency)(LPDWORD) PURE;
    STDMETHOD(GetScanLine)(LPDWORD) PURE;
    STDMETHOD(GetVerticalBlankStatus)(LPBOOL) PURE;
    STDMETHOD(Initialize)(GUID*) PURE;                                               // 0x48
    STDMETHOD(RestoreDisplayMode)() PURE;                                            // 0x4C
    STDMETHOD(SetCooperativeLevel)(HWND, DWORD) PURE;                                // 0x50
    STDMETHOD(SetDisplayMode)(DWORD, DWORD, DWORD, DWORD, DWORD) PURE;
    STDMETHOD(WaitForVerticalBlank)(DWORD, HANDLE) PURE;
    STDMETHOD(GetAvailableVidMem)(DDSCAPS2*, LPDWORD, LPDWORD) PURE;
    STDMETHOD(GetSurfaceFromDC)(HDC, IDirectDrawSurface7**) PURE;
    STDMETHOD(RestoreAllSurfaces)() PURE;
    STDMETHOD(TestCooperativeLevel)() PURE;
    STDMETHOD(GetDeviceIdentifier)(void*, DWORD) PURE;
    STDMETHOD(StartModeTest)(LPSIZE, DWORD, DWORD) PURE;
    STDMETHOD(EvaluateMode)(DWORD, DWORD*) PURE;
};

extern "C" const GUID CLSID_DirectDraw7;    // 0x635B7C
extern "C" const GUID IID_IDirectDraw7;     // 0x635B60

#endif
