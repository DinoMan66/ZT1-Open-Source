// sndsoundwav.h - SNDSoundResourceWAV: a .wav file loaded as one block.
// vtable at 0x6351AC: 0 dtor 0x41E5C5, 2 attempt 0x41C4C2, 4 0x4072A3, 5 isValid 0x40733D, 7 getSize 0x41C789, 8-15 getters below.
#ifndef SNDSOUNDWAV_H
#define SNDSOUNDWAV_H
#include "sndsoundresource.h"

struct SNDWavHeader                  // canonical 44-byte RIFF/WAVE header
{
    DWORD mRiff;                      // "RIFF"
    DWORD mRiffSize;
    DWORD mWave;                      // "WAVE"
    DWORD mFmt;                       // "fmt "
    WORD  mFmtSize;                   // +0x10 (low word of the fmt chunk size)
    WORD  mFmtSizeHigh;
    WORD  wFormatTag;                 // +0x14
    WORD  nChannels;                  // +0x16
    DWORD nSamplesPerSec;             // +0x18
    DWORD nAvgBytesPerSec;            // +0x1C
    WORD  nBlockAlign;                // +0x20
    WORD  wBitsPerSample;             // +0x22
    DWORD mData;                      // "data"
    DWORD mDataSize;
};

class SNDSoundResourceWAV : public SNDSoundResource
{
public:
    bool  attempt(DX8SndMgr* owner, const char* name);   // 0x41C4C2
    bool  isValid();                                         // 0x40733D
    DWORD getSize();
    WORD  getCbSize();
    DWORD getAvgBytesPerSec();
    WORD  getBlockAlign();
    WORD  getNumChannels();
    DWORD getSampleRate();
    WORD  getBitsPerSample();
    WORD  getFormatTag();
    void* data();

    SNDWavHeader* mHeader;            // +0x08
    void*         mData;              // +0x0C
};

#endif
