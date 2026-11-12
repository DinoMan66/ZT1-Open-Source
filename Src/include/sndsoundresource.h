// sndsoundresource.h - SNDSoundResource: base class of sound resources (WAV etc.).
// Virtual slots (vtable at 0x635218): 0 dtor 0x61FF34, 1 0x460FFE (forwards to attempt), 2 attempt 0x61FF52,
// 3 0x61FFAF, 4 0x4072FA, 5 0x62000B, 6 0x61F8C0 (shared with GXImage - a common base), 7 0x620029,
// 8-15 the WAVEFORMATEX getters below.
#ifndef SNDSOUNDRESOURCE_H
#define SNDSOUNDRESOURCE_H
#include <windows.h>
#include "BFLog.h"
#include "dx8sndmgr.h"

struct BFResourceEntry               // reference-counted data block (same layout as BFRefDataBase in bfrefdata.h)
{
    DWORD mUnknown0;                 // +0x00: reference count
    DWORD mUnknown4;
    DWORD mUnknown8;
    void* mData;                     // +0x0C: the loaded bytes
    DWORD mSize;                     // +0x10: size in bytes

    void addRef();                   // 0x4038F2
    void release();                  // 0x407330: drops one reference, frees the data with the last one
    void freeData();                 // 0x402EC7
};

class BFResourceHandle               // smart handle to a BFResourceEntry
{
public:
    bool load(const char* name);     // 0x403891 [name guessed: the callers log "load failed" when it returns false]
    bool f4047f4(const char* name);  // 0x4047F4 (name unknown): sibling of load(), called by SNDSoundResource::vf3
    void set(BFResourceEntry* entry);   // 0x407306 (name: guess)
    ~BFResourceHandle() { reset(); }
    void reset();                        // name: guess; out of line, BBT pastes it into the callers
    void* getData() { return mEntry ? mEntry->mData : 0; }

    BFResourceEntry* mEntry;
};

class SNDSoundResource
{
public:
    virtual ~SNDSoundResource();
    virtual bool  vf1(DX8SndMgr* owner, const char* name);
    virtual bool  attempt(DX8SndMgr* owner, const char* name);   // 0x61FF52
    virtual int   vf3(DX8SndMgr* owner, const char* name);   // returns 0 / 1 (`mov eax,1` in the original)
    virtual void  vf4();
    virtual bool  isValid();          // 0x62000B (slot 5)
    virtual DWORD vf6();
    virtual DWORD getSize();          // 0x620029 (slot 7): resource size in bytes
    virtual WORD  getCbSize();
    virtual DWORD getAvgBytesPerSec();
    virtual WORD  getBlockAlign();
    virtual WORD  getNumChannels();
    virtual DWORD getSampleRate();
    virtual WORD  getBitsPerSample();
    virtual WORD  getFormatTag();
    virtual void* data();

    BFResourceHandle mHandle;         // +0x04
};

#endif
