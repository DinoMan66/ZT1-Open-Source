// bfdsound.h - the DirectSound 8 declarations zoo.exe uses (vtable order as in dsound.h, DX8).
#ifndef BFDSOUND_H
#define BFDSOUND_H
#include <windows.h>
#include <objbase.h>
#include <mmsystem.h>

#define DSBSTATUS_PLAYING     0x00000001
#define DSBSTATUS_BUFFERLOST  0x00000002
#define DSBPLAY_LOOPING       0x00000001

struct IDirectSoundBuffer8 : public IUnknown
{
    STDMETHOD(GetCaps)(void*) PURE;
    STDMETHOD(GetCurrentPosition)(LPDWORD, LPDWORD) PURE;
    STDMETHOD(GetFormat)(LPWAVEFORMATEX, DWORD, LPDWORD) PURE;
    STDMETHOD(GetVolume)(LPLONG) PURE;                                      // 0x18
    STDMETHOD(GetPan)(LPLONG) PURE;
    STDMETHOD(GetFrequency)(LPDWORD) PURE;
    STDMETHOD(GetStatus)(LPDWORD) PURE;                                     // 0x24
    STDMETHOD(Initialize)(void*, void*) PURE;
    STDMETHOD(Lock)(DWORD, DWORD, LPVOID*, LPDWORD, LPVOID*, LPDWORD, DWORD) PURE;
    STDMETHOD(Play)(DWORD, DWORD, DWORD) PURE;                              // 0x30
    STDMETHOD(SetCurrentPosition)(DWORD) PURE;
    STDMETHOD(SetFormat)(LPCWAVEFORMATEX) PURE;
    STDMETHOD(SetVolume)(LONG) PURE;                                        // 0x3C
    STDMETHOD(SetPan)(LONG) PURE;                                           // 0x40
    STDMETHOD(SetFrequency)(DWORD) PURE;
    STDMETHOD(Stop)() PURE;                                                 // 0x48
    STDMETHOD(Unlock)(LPVOID, DWORD, LPVOID, DWORD) PURE;
    STDMETHOD(Restore)() PURE;
    STDMETHOD(SetFX)(DWORD, void*, LPDWORD) PURE;
    STDMETHOD(AcquireResources)(DWORD, DWORD, LPDWORD) PURE;
    STDMETHOD(GetObjectInPath)(REFGUID, DWORD, REFGUID, LPVOID*) PURE;
};
#endif
