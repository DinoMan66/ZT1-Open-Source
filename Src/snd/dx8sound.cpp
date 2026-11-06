// dx8sound.cpp - DX8Sound (original: C:\aqua\src\snd\dx8sound.cpp).
#include "dx8sound.h"

// 0x61FD37
bool DX8Sound::init(SNDSoundGroup* owner, const char* name)
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
bool DX8Sound::instantiateFor(SNDSoundGroup* owner)
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

// 0x40757B  COMPILER-LIMITED (re-checked round 239): load order of the attenuation sum. An inline helper for
//           the sum / the buffer condition and an early-return form gave the same difference.
void DX8Sound::setVolume(long volume)
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->mVolume + mVolumeB + mVolumeA + volume;
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

// 0x4FFC6B  COMPILER-LIMITED (re-checked round 239): the original negates, then subtracts each term; a
//           sequenced statement form and a named volume local gave the same difference.
void DX8Sound::mute()
{
    mSavedVolume = -getVolume() - mVolumeB - mVolumeA - g_sndMgr->mVolume;
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

// 0x44369A  COMPILER-LIMITED (re-checked round 239): mBuffer is tested in ecx (original eax) and kept live;
//           inline helpers and an early return did not change it. Same for playLooped.
void DX8Sound::play()
{
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->mVolume + mVolumeB + mVolumeA;
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

// 0x4FC592
void DX8Sound::playLooped()
{
    mLooping = true;
    if (mBuffer || (prepare() && mBuffer))
    {
        long attenuation = g_sndMgr->mVolume + mVolumeB + mVolumeA;
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
