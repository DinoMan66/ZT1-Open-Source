// sndsoundresource.cpp - SNDSoundResource (original: C:\aqua\src\snd\sndsoundresource.cpp).
#include "sndsoundresource.h"

// 0x61FF52
// name: string ("SNDSoundResource::attempt(%s) - load failed")
bool SNDSoundResource::attempt(DX8SndMgr* owner, const char* name)
{
    vf4();
    if (!owner->isValid())
        return false;
    if (!mHandle.load(name))
    {
#line 53 "C:\\aqua\\src\\snd\\sndsoundresource.cpp"
        BFLog(BFLOG_ARGS(BFLOG_NOTE), "SNDSoundResource::attempt(%s) - load failed", name);
        return false;
    }
    return true;
}

// 0x62000B
bool SNDSoundResource::isValid()
{
    return mHandle.mEntry && mHandle.mEntry->mUnknown4 && mHandle.mEntry->mUnknown8;
}

// 0x620029
DWORD SNDSoundResource::getSize()
{
    return mHandle.mEntry ? mHandle.mEntry->mSize : 0;
}

// 0x620037
WORD SNDSoundResource::getCbSize()
{
#line 89 "C:\\aqua\\src\\snd\\sndsoundresource.cpp"
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getCbSize unimplemented");
    return 0;
}

// 0x62005D
DWORD SNDSoundResource::getAvgBytesPerSec()
{
#line 96
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getAvgBytesPerSec unimplemented");
    return 0;
}

// 0x620082
WORD SNDSoundResource::getBlockAlign()
{
#line 103
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getBlockAlign unimplemented");
    return 0;
}

// 0x6200A8
WORD SNDSoundResource::getNumChannels()
{
#line 110
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getNumChannels unimplemented");
    return 0;
}

// 0x6200CE
DWORD SNDSoundResource::getSampleRate()
{
#line 117
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getSampleRate unimplemented");
    return 0;
}

// 0x6200F3
WORD SNDSoundResource::getBitsPerSample()
{
#line 124
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getBitsPerSample unimplemented");
    return 0;
}

// 0x620119
WORD SNDSoundResource::getFormatTag()
{
#line 131
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::getFormatTag unimplemented");
    return 0;
}

// 0x620142
void* SNDSoundResource::data()
{
#line 139
    BFLog(BFLOG_ARGS(BFLOG_FATAL), "SNDSoundResource::data unimplemented");
    return 0;
}

// 0x4038F2
void BFResourceEntry::addRef()
{
    ++mUnknown0;
}

// 0x407330
void BFResourceEntry::release()
{
    if (--mUnknown0 == 0)
        freeData();
}

// 0x407306
void BFResourceHandle::set(BFResourceEntry* entry)
{
    if (entry == mEntry)
        return;
    if (mEntry)
        mEntry->release();
    mEntry = entry;
    if (entry)
        entry->addRef();
}

// no standalone body in zoo.exe (BBT pasted it into its callers; name: guess)
void BFResourceHandle::reset()
{
    set(0);
}

// slot 4, 0x4072FA: drops the loaded data
void SNDSoundResource::vf4()
{
    mHandle.reset();
}

// 0x41E5E3: the destructor body (the deleting wrapper is the vtable's slot 0, 0x61FF34); mHandle's destructor follows
SNDSoundResource::~SNDSoundResource()
{
    vf4();
}

// 0x460FFE  slot 1: forwards to attempt (slot 2)
bool SNDSoundResource::vf1(DX8SndMgr* owner, const char* name)
{
    return attempt(owner, name);
}

// 0x61F8C0  slot 6 (name unknown): a field of the loaded entry
DWORD SNDSoundResource::vf6()
{
    return mHandle.mEntry ? mHandle.mEntry->mUnknown8 : 0;
}

// 0x61FFAF  slot 3: loads the named resource; a complete entry is then attempted through slot 2
int SNDSoundResource::vf3(DX8SndMgr* owner, const char* name)
{
    vf4();
    if (!mHandle.f4047f4(name))
        return 0;
    BFResourceEntry* entry = mHandle.mEntry;
    if (entry && entry->mUnknown4 && entry->mUnknown8 && entry->mData)
    {
        if (!attempt(owner, name))
            return 0;
    }
    return 1;
}
