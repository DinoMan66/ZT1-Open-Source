// sndsoundwav.cpp - SNDSoundResourceWAV (original: C:\aqua\src\snd\sndsoundwav.cpp).
#include "sndsoundwav.h"

// 0x41C789: the sample data size = resource size minus the 44-byte header
DWORD SNDSoundResourceWAV::getSize()
{
    return (mEntry ? mEntry->mSize : 0) - sizeof(SNDWavHeader);
}

WORD  SNDSoundResourceWAV::getCbSize()         { return mHeader->mFmtSize; }        // 0x41C7AB
DWORD SNDSoundResourceWAV::getAvgBytesPerSec() { return mHeader->nAvgBytesPerSec; } // 0x41C7B3
WORD  SNDSoundResourceWAV::getBlockAlign()     { return mHeader->nBlockAlign; }     // 0x41C7BA
WORD  SNDSoundResourceWAV::getNumChannels()    { return mHeader->nChannels; }       // 0x41C7C2
DWORD SNDSoundResourceWAV::getSampleRate()     { return mHeader->nSamplesPerSec; }  // 0x41C7CA
WORD  SNDSoundResourceWAV::getBitsPerSample()  { return mHeader->wBitsPerSample; }  // 0x41C79B
WORD  SNDSoundResourceWAV::getFormatTag()      { return mHeader->wFormatTag; }      // 0x41C7A3
void* SNDSoundResourceWAV::data()              { return mData; }                    // 0x407378
