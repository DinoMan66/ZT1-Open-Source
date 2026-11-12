// dx8sound.h - DX8Sound: one sound effect playing through a DirectSound 8 buffer.
// vtable at 0x63506C (slot order below). Names in [brackets] are guesses.
#ifndef DX8SOUND_H
#define DX8SOUND_H
#include "bfdsound.h"
#include "BFLog.h"
#include "dx8sndmgr.h"

class SNDSoundResource;

struct BFPos;                            // [layout unknown] only passed by pointer

class DX8Sound
{
public:
    virtual ~DX8Sound();                                      // 0  0x41E3DA
    virtual bool init(DX8SndMgr* owner, const char* name); // 1  0x61FD37
    virtual bool load(DX8SndMgr* owner, const char* name); // 2  0x406F83
    virtual bool load2(DX8SndMgr* owner, const char* name);// 3  0x406F83 (same body)
    virtual void release();                                   // 4  0x4029D5
    virtual bool hasName();                                   // 5  0x4074D3
    virtual const char* getName();                            // 6  0x407374
    virtual DX8SndMgr* getManager();                          // 7  0x57D5E1
    virtual bool instantiateFor(DX8SndMgr* owner);        // 8  0x41C77C
    virtual void play(BFPos* pos);                            // 9  0x440764 [name: log strings]
    virtual void play(long volume);                           // 10 0x61FD4C
    virtual void play();                                      // 11 0x44369A
    virtual void updatePosition(BFPos* pos);                  // 12 0x44153B [name: log strings]
    virtual void playLooped(BFPos* pos);                      // 13 0x441797 [name: log strings]
    virtual void playLooped(long volume);                     // 14 0x61FE0E
    virtual void playLooped();                                // 15 0x4FC592
    virtual void setVolume(long volume);                      // 16 0x40757B
    virtual long getVolume();                                 // 17 0x4FFC9F
    virtual void setVolumeA(long v);                          // 18 0x407523
    virtual void setVolumeB(long v);                          // 19 0x407555
    virtual bool isPlaying();                                 // 20 0x40747C
    virtual int  notifyOwner();                               // 21 0x41E31E
    virtual void mute();                                      // 22 0x4FFC6B
    virtual void unmute();                                    // 23 0x4FFD3A
    virtual void stop();                                      // 24 0x41ED99

    bool isLost();                                            // 0x41E795
    bool prepare();                                           // 0x41C488 [name guessed]
    bool loadResource();                                      // 0x41C514 ("could not load %s")
    bool instantiate(DX8SndMgr* owner);                   // 0x41C5A4
    void releaseBuffer();                                     // name: guess; BBT pastes it into release() (0x4029D5)
    void releaseResource();                                   // name: guess; BBT pastes it into release() (0x4029D5)

    const char*          mName;          // +0x04
    SNDSoundResource*    mResource;      // +0x08
    IDirectSoundBuffer8* mBuffer;        // +0x0C
    DX8SndMgr*       mOwner;         // +0x10
    long                 mVolumeA;       // +0x14
    long                 mVolumeB;       // +0x18
    bool                 mLooping;       // +0x1C
    long                 mSavedVolume;   // +0x20: used by mute/unmute
};

#endif
