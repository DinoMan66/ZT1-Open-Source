// sndsoundresource.cpp - SNDSoundResource (original: C:\aqua\src\snd\sndsoundresource.cpp).
#include "sndsoundresource.h"

// 0x62000B
int SNDSoundResource::isValid()
{
    return mEntry && mEntry->mUnknown4 && mEntry->mUnknown8;
}

// 0x620029
DWORD SNDSoundResource::getSize()
{
    return mEntry ? mEntry->mSize : 0;
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
