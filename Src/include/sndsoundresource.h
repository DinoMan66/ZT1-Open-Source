// sndsoundresource.h - SNDSoundResource: base class of sound resources (WAV etc.).
// Virtual slots (vtable at 0x635218): 0 dtor 0x61FF34, 2 attempt 0x61FF52, 3 0x61FFAF,
// 5 0x62000B, 6 0x61F8C0 (shared with GXImage - a common base), 7 0x620029,
// 8-15 the WAVEFORMATEX getters below.
#ifndef SNDSOUNDRESOURCE_H
#define SNDSOUNDRESOURCE_H
#include <windows.h>
#include "BFLog.h"

struct BFResourceEntry               // what the resource handle at +4 points to (fields partly known)
{
    DWORD mUnknown0;
    DWORD mUnknown4;
    DWORD mUnknown8;
    DWORD mUnknownC;
    DWORD mSize;          // +0x10: size in bytes
};

class SNDSoundResource
{
public:
    virtual ~SNDSoundResource();
    int   isValid();                  // 0x62000B (slot 5)
    DWORD getSize();                  // 0x620029 (slot 7): resource size in bytes
    WORD  getCbSize();
    DWORD getAvgBytesPerSec();
    WORD  getBlockAlign();
    WORD  getNumChannels();
    DWORD getSampleRate();
    WORD  getBitsPerSample();
    WORD  getFormatTag();
    void* data();

    BFResourceEntry* mEntry;          // +0x04 (first member of an embedded resource handle)
};

#endif
