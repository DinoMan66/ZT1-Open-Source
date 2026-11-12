// gximage.h - GXImage: an image of either file format. It owns one loader object (GXImageTGA or
// GXImageBMP, picked from the last letter of the file name in attempt, 0x4B3223) and forwards the
// questions about the picture to it. Vtable at 0x630C24.
// name: guess (the shared base of the image classes; SNDSoundResource's slot 6 shares its code, 0x61F8C0)
#ifndef GXIMAGE_H
#define GXIMAGE_H

class GXCanvas;

// The loader object behind a GXImage: the layout of the vtables of GXImageTGA (0x6351EC) and
// GXImageBMP (0x63585C).
class GXImageSource
{
public:
    virtual ~GXImageSource();
    virtual bool vf1(const char* name);
    virtual bool attempt(const char* name);
    virtual void release();
    virtual bool isValid();
    virtual int getWidth();
    virtual int getHeight();
    virtual int getDepth();
    virtual int vf8();
    virtual int vf9(void* a);
    virtual bool vf10(GXCanvas* canvas, int x, int y);
};

class GXImage
{
public:
    GXImage();                                   // 0x40D889
    virtual ~GXImage();                          // 0x40D952
    virtual bool vf1(const char* name);          // 0x4B3216: forwards to attempt
    virtual bool attempt(const char* name);      // 0x4B3223
    virtual void release();                      // 0x402876
    virtual bool isValid();                      // 0x4B3685
    virtual int getWidth();                      // 0x4B3297
    virtual int getHeight();                     // 0x4B3287
    virtual int getDepth();                      // 0x61EF92
    virtual int vf8();                           // 0x61EFA1
    virtual int vf9(void* a);                    // 0x61EFB0
    virtual bool vf10(GXCanvas* canvas, int x, int y);   // 0x40D8BF: draws the picture into the canvas

    GXImageSource* m_source;                     // 0x04
};

#endif
