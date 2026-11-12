// dx8sndmgr.h - DX8SndMgr: the DirectSound sound manager (original: C:\aqua\src\snd\dx8sndmgr.cpp).
// vtable at 0x630A48. It is also what DX8Sound::mOwner and SNDSoundResource::attempt take: instantiate()
// reads its IDirectSound pointer at +0x1C. Only the members and slots used so far are named.
#ifndef DX8SNDMGR_H
#define DX8SNDMGR_H
#include "bfdsound.h"
#include "BFLog.h"

class DX8Sound;

class DX8SndMgr
{
public:
    virtual void vf0();                         // 0x61FEEC
    virtual void vf1(); virtual void vf2(); virtual void vf3();
    virtual bool vf4(DX8Sound* sound, const char* name);    // slot 4 (0x10) 0x5FED6A forwards to load
    virtual bool load(DX8Sound* sound, const char* name);   // slot 5 (0x14) 0x61FF0A [name: forwards to DX8Sound::load]
    virtual bool instantiateFor(DX8Sound* sound);           // slot 6 (0x18) 0x61FF20 [name: forwards to DX8Sound::instantiateFor]
    virtual void vf7(int arg);                 // slot 7 (0x1C) 0x404FCF: does nothing
    virtual bool attach(DX8Sound* sound);       // slot 8  (0x20) [name guessed]
    virtual int  notify(DX8Sound* sound);       // slot 9  (0x24) [name guessed]
    virtual bool vf10();                        // slot 10 (0x28) 0x406F7F: returns the flag at +0x18
    virtual bool isValid();                     // slot 11 (0x2C) 0x404A7E [name: the log string "sound manager not valid"]
    virtual void vf12(); virtual void vf13(); virtual void vf14();
    virtual void vf15(DX8Sound* sound);         // slot 15 (0x3C): called when a positioned sound is out of range

    long getVolume();                    // 0x404FC0 [name guessed]; out of line, BBT inlines it into most callers
    bool createDirectSound(HWND hwnd);   // 0x527751 [name from the log string "succeeded at createDirectSound"]
    bool setPrimaryBufferFormat(DWORD channels, DWORD freq, DWORD bits);   // 0x527BF9 [name: log strings]
    bool createDirectSoundForApp();      // 0x5277C2 [name: guess; createDirectSound with the application window]
    void f57da5b();                      // 0x57DA5B (name unknown): cleanup after a failed createDirectSound

    DWORD mUnknown4[4];                  // +0x04 .. +0x13
    long  mVolume;                       // +0x14: master attenuation
    bool  mUnknown18;
    IDirectSound* mDirectSound;          // +0x1C
};

extern DX8SndMgr* g_sndMgr;              // 0x6380A8

#endif
