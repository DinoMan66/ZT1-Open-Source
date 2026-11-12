// dx8sndmgr.cpp - DX8SndMgr (original: C:\aqua\src\snd\dx8sndmgr.cpp).
#include <string.h>
#include "dx8sound.h"
#include "bfapp.h"

// 0x404FC0  the master attenuation; called out of line (BBT pastes it into most callers)
long DX8SndMgr::getVolume()
{
    return mVolume;
}

// 0x5FED6A  slot 4: forwards to load (name unknown)
bool DX8SndMgr::vf4(DX8Sound* sound, const char* name)
{
    return load(sound, name);
}

// 0x404FCF  slot 7 (purpose unknown): nothing to do in the base manager
void DX8SndMgr::vf7(int arg)
{
}

// 0x406F7F  slot 10 (purpose unknown)
bool DX8SndMgr::vf10()
{
    return mUnknown18;
}

// 0x61FF0A  name: forwards to DX8Sound::load, which takes the manager as its owner
bool DX8SndMgr::load(DX8Sound* sound, const char* name)
{
    return sound->load(this, name);
}

// 0x61FF2F  name: guess (caller DX8Sound::prepare treats the result as success); the vtable shares this stub
//           with slots 9 and 15, so the base manager attaches nothing
bool DX8SndMgr::attach(DX8Sound* sound)
{
    return false;
}

// 0x61FF20  name: forwards to DX8Sound::instantiateFor
bool DX8SndMgr::instantiateFor(DX8Sound* sound)
{
    return sound->instantiateFor(this);
}

// 0x52770B (name unknown): creates the DirectSound object and initialises it on the default device
static HRESULT f52770b(IDirectSound** ppDS)
{
    CoInitialize(NULL);
    HRESULT hr = CoCreateInstance(CLSID_DirectSound, NULL,
                                  CLSCTX_INPROC_SERVER | CLSCTX_INPROC_HANDLER | CLSCTX_LOCAL_SERVER,
                                  IID_IDirectSound, (void**)ppDS);
    if (SUCCEEDED(hr))
    {
        hr = (*ppDS)->Initialize(NULL);
        if (FAILED(hr))
        {
#line 56 "C:\\aqua\\src\\snd\\dx8sndmgr.cpp"
            BFLogHR(BFLOG_HR_ARGS(hr), "Initialize");
            (*ppDS)->Release();
            CoUninitialize();
        }
    }
    else
    {
#line 60
        BFLogHR(BFLOG_HR_ARGS(hr), "::CoCreateInstance");
        CoUninitialize();
    }
    return hr;
}

// 0x527751  name: string ("succeeded at createDirectSound")
bool DX8SndMgr::createDirectSound(HWND hwnd)
{
    if (SUCCEEDED(f52770b(&mDirectSound)))
    {
        HRESULT hr = mDirectSound->SetCooperativeLevel(hwnd, DSSCL_PRIORITY);
        if (SUCCEEDED(hr))
        {
            if (setPrimaryBufferFormat(2, 22050, 16))
            {
#line 82
                BFLog(BFLOG_ARGS(BFLOG_NOTE), "succeeded at createDirectSound");
                return true;
            }
#line 85
            BFLog(BFLOG_ARGS(BFLOG_ERROR),
                  "setPrimaryBufferFormat: dwPrimaryChannels %d, dwPrimaryFreq %d, dwPrimaryBitRate %d", 2, 22050, 16);
        }
        else
        {
#line 89
            BFLogHR(BFLOG_HR_ARGS(hr), "SetCooperativeLevel: HWND %d dwCoopLevel %d", hwnd, DSSCL_PRIORITY);
        }
        f57da5b();
        return false;
    }
    mDirectSound = NULL;
    return false;
}

// 0x527BF9  name: string ("setPrimaryBufferFormat CO_E_NOTINITIALIZED" etc.)
// The same steps as the DirectSound SDK sample of that name (dsutil.cpp).
bool DX8SndMgr::setPrimaryBufferFormat(DWORD channels, DWORD freq, DWORD bits)
{
    IDirectSoundBuffer8* primary = NULL;
    if (!mDirectSound)
    {
#line 125
        BFLog(BFLOG_ARGS(BFLOG_ERROR), "setPrimaryBufferFormat CO_E_NOTINITIALIZED");
        return false;
    }
    DSBUFFERDESC desc;
    memset(&desc, 0, sizeof(desc));
    desc.dwSize = sizeof(DSBUFFERDESC);
    desc.dwFlags = DSBCAPS_PRIMARYBUFFER;
    desc.dwBufferBytes = 0;
    desc.lpwfxFormat = NULL;
    HRESULT hr = mDirectSound->CreateSoundBuffer(&desc, &primary, NULL);
    if (SUCCEEDED(hr))
    {
        WAVEFORMATEX wfx;
        memset(&wfx, 0, sizeof(wfx));
        wfx.wFormatTag = WAVE_FORMAT_PCM;
        wfx.nChannels = (WORD)channels;
        wfx.nSamplesPerSec = freq;
        wfx.wBitsPerSample = (WORD)bits;
        wfx.nBlockAlign = (WORD)(wfx.wBitsPerSample / 8 * wfx.nChannels);
        wfx.nAvgBytesPerSec = wfx.nSamplesPerSec * wfx.nBlockAlign;
        hr = primary->SetFormat(&wfx);
        if (FAILED(hr))
        {
#line 151
            BFLogHR(BFLOG_HR_ARGS(hr),
                    "setPrimaryBufferFormat SetFormat: dwPrimaryChannels %d dwPrimaryFreq %d dwPrimaryBitRate %d",
                    channels, freq, bits);
            return false;
        }
        primary->Release();
        return true;
    }
#line 155
    BFLogHR(BFLOG_HR_ARGS(hr), "setPrimaryBufferFormat CreateSoundBuffer");
    return false;
}

// 0x5277C2
bool DX8SndMgr::createDirectSoundForApp()
{
    return createDirectSound(BFGetApp()->m_hwnd);
}
