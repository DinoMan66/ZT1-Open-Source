// dx8sound.cpp - DX8Sound (original: C:\aqua\src\snd\dx8sound.cpp).
#include <string.h>
#include "dx8sound.h"
#include "sndsoundresource.h"

// 0x43F5BA (name unknown): volume and pan for a sound at a position
void f43f5ba(const BFPos* pos, long* volume, long* pan);

// 0x61FD37
bool DX8Sound::init(DX8SndMgr* owner, const char* name)
{
    mOwner = owner;
    return DX8Sound::load(owner, name);
}

// 0x4074D3
bool DX8Sound::hasName()
{
    return mName != 0;
}

// 0x407374
const char* DX8Sound::getName()
{
    return mName;
}

// 0x57D5E1
DX8SndMgr* DX8Sound::getManager()
{
    return g_sndMgr;
}

// 0x41C77C
bool DX8Sound::instantiateFor(DX8SndMgr* owner)
{
    return instantiate(owner);
}

// 0x41C488
bool DX8Sound::prepare()
{
    if (!mResource && !loadResource())
        return false;
    if (!instantiateFor(mOwner))
        return false;
    return mOwner->attach(this) ? true : false;
}

// 0x40747C  needs SP4: [esp] encoding only.
bool DX8Sound::isPlaying()
{
    if (mBuffer)
    {
        DWORD status;
        HRESULT hr = mBuffer->GetStatus(&status);
        if (FAILED(hr))
#line 397 "C:\\aqua\\src\\snd\\dx8sound.cpp"
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::isPlaying GetStatus failed");
        else if (status & DSBSTATUS_PLAYING)
            return true;
    }
    return false;
}

// 0x41E795  needs SP4: [esp] encoding only.
bool DX8Sound::isLost()
{
    if (mBuffer)
    {
        DWORD status;
        HRESULT hr = mBuffer->GetStatus(&status);
        if (FAILED(hr))
#line 413
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::isLost GetStatus failed");
        else if (status & DSBSTATUS_BUFFERLOST)
            return true;
    }
    return false;
}

// 0x40757B
void DX8Sound::setVolume(long volume)
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->getVolume() + mVolumeB + mVolumeA + volume;
        if (attenuation < 0)
            attenuation = 1;
        HRESULT hr = mBuffer->SetVolume(-attenuation);
        if (FAILED(hr))
#line 433
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::setVolume SetVolume to %d failed for %s", attenuation, getName());
    }
}

// 0x4FFC9F  The early `return 0` is what keeps mBuffer in eax: on that path the compiler returns the
//           null pointer itself as the 0 (round 239).
long DX8Sound::getVolume()
{
    long volume;
    if (!mBuffer)
        return 0;
    volume = 0;
    mBuffer->GetVolume(&volume);
    return volume;
}

// 0x407523
void DX8Sound::setVolumeA(long v)
{
    mVolumeA = v;
}

// 0x407555
void DX8Sound::setVolumeB(long v)
{
    mVolumeB = v;
}

// 0x41E31E
int DX8Sound::notifyOwner()
{
    return mOwner->notify(this);
}

// 0x4FFC6B  remembers the attenuation that unmute() hands back to setVolume()
void DX8Sound::mute()
{
    long volume = -getVolume();
    mSavedVolume = volume - mVolumeB - mVolumeA - g_sndMgr->getVolume();
    setVolume(5000);
}

// 0x4FFD3A
void DX8Sound::unmute()
{
    setVolume(mSavedVolume);
}

// 0x41ED99
void DX8Sound::stop()
{
    if (mBuffer)
        mBuffer->Stop();
}

// 0x44369A
void DX8Sound::play()
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->getVolume() + mVolumeB + mVolumeA;
        if (attenuation < 0)
            attenuation = 1;
        if (attenuation != 0)
        {
            if (attenuation > 6000)
                return;
            HRESULT hr = mBuffer->SetVolume(-attenuation);
            if (FAILED(hr))
#line 186
                BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play setVolume failed for %s", getName());
        }
        HRESULT hr = mBuffer->Play(0, 0, 0);
        if (FAILED(hr))
#line 193
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play Play failed for %s", getName());
    }
}

// 0x61FD4C  play at an extra attenuation
void DX8Sound::play(long volume)
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->getVolume() + mVolumeB + mVolumeA + volume;
        if (attenuation < 0)
            attenuation = 1;
        if (attenuation > 6000)
            return;
        HRESULT hr = mBuffer->SetVolume(-attenuation);
        if (FAILED(hr))
#line 214
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play setVolume failed for %s", getName());
        hr = mBuffer->Play(0, 0, 0);
        if (FAILED(hr))
#line 220
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play(long) Play failed for %s", getName());
    }
}

// 0x4FC592
void DX8Sound::playLooped()
{
    mLooping = true;
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->getVolume() + mVolumeB + mVolumeA;
        if (attenuation < 0)
            attenuation = 1;
        if (attenuation != 0)
        {
            if (attenuation > 6000)
                return;
            HRESULT hr = mBuffer->SetVolume(-attenuation);
            if (FAILED(hr))
#line 306
                BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped setVolume failed for %s", getName());
        }
        HRESULT hr = mBuffer->Play(0, 0, DSBPLAY_LOOPING);
        if (FAILED(hr))
#line 313
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped Play failed for %s", getName());
    }
}

// 0x61FE0E  play looped at an extra attenuation
void DX8Sound::playLooped(long volume)
{
    mLooping = true;
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->getVolume() + mVolumeB + mVolumeA + volume;
        if (attenuation < 0)
            attenuation = 1;
        if (attenuation > 6000)
            return;
        HRESULT hr = mBuffer->SetVolume(-attenuation);
        if (FAILED(hr))
#line 335
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped setVolume failed for %s", getName());
        hr = mBuffer->Play(0, 0, DSBPLAY_LOOPING);
        if (FAILED(hr))
#line 341
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped(long) Play failed for %s", getName());
    }
}

// 0x440764
void DX8Sound::play(BFPos* pos)
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long volume;
        long pan;
        f43f5ba(pos, &volume, &pan);
        volume += g_sndMgr->getVolume() + mVolumeB + mVolumeA;
        if (volume < 0)
            volume = 1;
        if (volume > 6000)
            return;
        HRESULT hr = mBuffer->SetVolume(-volume);
        if (FAILED(hr))
#line 243
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play SetVolume failed for %s", getName());
        hr = mBuffer->SetPan(pan);
        if (FAILED(hr))
#line 247
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play SetPan failed for %s", getName());
        hr = mBuffer->Play(0, 0, 0);
        if (FAILED(hr))
#line 253
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::play(BFPos) Play failed for %s", getName());
    }
}

// 0x44153B
void DX8Sound::updatePosition(BFPos* pos)
{
    long volume;
    long pan;
    f43f5ba(pos, &volume, &pan);
    volume += g_sndMgr->getVolume() + mVolumeB + mVolumeA;
    if (volume < 0)
        volume = 1;
    if (volume > 9000)
    {
        stop();
        mOwner->vf15(this);
        return;
    }
    if (!mBuffer && !prepare())
        return;
    HRESULT hr = mBuffer->SetVolume(-volume);
    if (FAILED(hr))
#line 280
        BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::updatePosition SetVolume failed for %s", getName());
    hr = mBuffer->SetPan(pan);
    if (FAILED(hr))
#line 284
        BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::updatePosition SetPan failed for %s", getName());
}

// 0x441797
void DX8Sound::playLooped(BFPos* pos)
{
    mLooping = true;
    if (mBuffer || (prepare() && mBuffer))
    {
        long volume;
        long pan;
        f43f5ba(pos, &volume, &pan);
        volume += g_sndMgr->getVolume() + mVolumeB + mVolumeA;
        if (volume < 0)
            volume = 1;
        if (volume > 6000)
            return;
        HRESULT hr = mBuffer->SetVolume(-volume);
        if (FAILED(hr))
#line 365
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped SetVolume failed for %s", getName());
        hr = mBuffer->SetPan(pan);
        if (FAILED(hr))
#line 369
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped SetPan failed for %s", getName());
        hr = mBuffer->Play(0, 0, DSBPLAY_LOOPING);
        if (FAILED(hr))
#line 375
            BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::playLooped(BFPos) Play failed for %s", getName());
    }
}

// 0x41C5A4  name: string ("DX8Sound::instantiate - %s, copy %d bytes")
// Creates the DirectSound buffer for the loaded resource and copies the sample data into it.
bool DX8Sound::instantiate(DX8SndMgr* mgr)
{
    if (!mResource || !mResource->isValid())
        return false;
    if (!mgr->isValid())
    {
        mBuffer = 0;
#line 479 "C:\\aqua\\src\\snd\\dx8sound.cpp"
        BFLog(BFLOG_ARGS(BFLOG_INFO), "sound manager not valid, so can't instantiate %s", getName());
        return false;
    }
    DWORD size = mResource->getSize();
    GUID guid3D = GUID_NULL;
    WAVEFORMATEX fmt;
    memset(&fmt, 0, sizeof(fmt));
    fmt.cbSize = mResource->getCbSize();
    fmt.nAvgBytesPerSec = mResource->getAvgBytesPerSec();
    fmt.nBlockAlign = mResource->getBlockAlign();
    fmt.nChannels = mResource->getNumChannels();
    fmt.nSamplesPerSec = mResource->getSampleRate();
    fmt.wBitsPerSample = mResource->getBitsPerSample();
    fmt.wFormatTag = mResource->getFormatTag();
    DSBUFFERDESC desc;
    memset(&desc, 0, sizeof(desc));
    desc.guid3DAlgorithm = guid3D;
    desc.dwSize = sizeof(DSBUFFERDESC);
    desc.dwFlags = DSBCAPS_CTRLPAN | DSBCAPS_CTRLVOLUME;
    desc.dwBufferBytes = size;
    desc.lpwfxFormat = &fmt;
    HRESULT hr = mgr->mDirectSound->CreateSoundBuffer(&desc, &mBuffer, NULL);
    if (SUCCEEDED(hr))
    {
        void* data;
        DWORD bytes;
        hr = mBuffer->Lock(0, size, &data, &bytes, NULL, NULL, 0);
        if (SUCCEEDED(hr))
        {
#line 512
            BFLog(BFLOG_ARGS(BFLOG_INFO), "DX8Sound::instantiate - %s, copy %d bytes", getName(), mResource->getSize());
            memcpy(data, mResource->data(), mResource->getSize());
            mBuffer->Unlock(data, bytes, NULL, 0);
            return true;
        }
#line 518
        BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::instantiate - Lock failed");
        mBuffer->Release();
        mBuffer = 0;
        return false;
    }
#line 522
    BFLogHR(BFLOG_HR_ARGS(hr), "DX8Sound::instantiate - CreateSoundBuffer failed");
    mBuffer = 0;
    return false;
}

// 0x4029D5  slot 4: drops the DirectSound buffer and the loaded resource
// name: vtable slot 4 in the DX8Sound vtable (0x63506C); the destructor 0x41E3A1 calls it (guess)
void DX8Sound::release()
{
    releaseBuffer();
    releaseResource();
}

// name: guess (two helpers whose bodies BBT pasted into release() and the destructor path at 0x41E500)
void DX8Sound::releaseBuffer()
{
    if (mBuffer)
    {
        mBuffer->Release();
        mBuffer = 0;
    }
}

void DX8Sound::releaseResource()
{
    if (mResource)
    {
        delete mResource;
        mResource = 0;
    }
}
