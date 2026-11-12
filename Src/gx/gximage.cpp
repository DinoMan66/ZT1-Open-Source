// gximage.cpp - GXImage (original: C:\aqua\src\gx\gximage.cpp): forwards to the loader object it owns.
#include "gximage.h"

// 0x4B3216  name: caller (GXImageTGA / GXImageBMP vtables share it as slot 1)
bool GXImage::vf1(const char* name)
{
    return attempt(name);
}

// 0x402876
void GXImage::release()
{
    if (!m_source)
        return;
    delete m_source;
    m_source = 0;
}

// 0x4B3685
// name: caller (the icon code tests it after loading, like GXImageTGA::isValid)
bool GXImage::isValid()
{
    return m_source && m_source->isValid();
}

// 0x4B3297
int GXImage::getWidth()
{
    if (m_source)
        return m_source->getWidth();
    return 0;
}

// 0x4B3287
int GXImage::getHeight()
{
    if (m_source)
        return m_source->getHeight();
    return 0;
}

// 0x61EF92
int GXImage::getDepth()
{
    if (m_source)
        return m_source->getDepth();
    return 0;
}

// 0x61EFA1
int GXImage::vf8()
{
    if (m_source)
        return m_source->vf8();
    return 0;
}

// 0x40D8BF
bool GXImage::vf10(GXCanvas* canvas, int x, int y)
{
    if (m_source)
        return m_source->vf10(canvas, x, y);
    return false;
}
