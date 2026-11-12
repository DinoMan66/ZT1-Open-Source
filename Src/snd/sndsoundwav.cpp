// sndsoundwav.cpp - SNDSoundResourceWAV (original: C:\aqua\src\snd\sndsoundwav.cpp).
#include "sndsoundwav.h"

// 0x41C4C2
// name: string ("SNDSoundResourceWAV::attempt(%s) - load failed")
bool SNDSoundResourceWAV::attempt(DX8SndMgr* owner, const char* name)
{
    if (!owner->isValid())
        return false;
    vf4();
    if (!mHandle.load(name))
    {
#line 69 "C:\\aqua\\src\\snd\\sndsoundwav.cpp"
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "SNDSoundResourceWAV::attempt(%s) - load failed", name);
        return false;
    }
    mHeader = mHandle.mEntry ? (SNDWavHeader*)mHandle.mEntry->mData : 0;
    mData = mHeader + 1;
    return true;
}

// 0x40733D: valid once the resource is loaded and the header and sample data pointers are set
// name: vtable (overrides SNDSoundResource::isValid, slot 5)
bool SNDSoundResourceWAV::isValid()
{
    return mHandle.mEntry && mHandle.mEntry->mUnknown4 && mHandle.mEntry->mUnknown8 && mHeader && mData;
}

// 0x41C789: the sample data size = resource size minus the 44-byte header
DWORD SNDSoundResourceWAV::getSize()
{
    return (mHandle.mEntry ? mHandle.mEntry->mSize : 0) - sizeof(SNDWavHeader);
}

WORD  SNDSoundResourceWAV::getCbSize()         { return mHeader->mFmtSize; }        // 0x41C7AB
DWORD SNDSoundResourceWAV::getAvgBytesPerSec() { return mHeader->nAvgBytesPerSec; } // 0x41C7B3
WORD  SNDSoundResourceWAV::getBlockAlign()     { return mHeader->nBlockAlign; }     // 0x41C7BA
WORD  SNDSoundResourceWAV::getNumChannels()    { return mHeader->nChannels; }       // 0x41C7C2
DWORD SNDSoundResourceWAV::getSampleRate()     { return mHeader->nSamplesPerSec; }  // 0x41C7CA
WORD  SNDSoundResourceWAV::getBitsPerSample()  { return mHeader->wBitsPerSample; }  // 0x41C79B
WORD  SNDSoundResourceWAV::getFormatTag()      { return mHeader->wFormatTag; }      // 0x41C7A3
void* SNDSoundResourceWAV::data()              { return mData; }                    // 0x407378
