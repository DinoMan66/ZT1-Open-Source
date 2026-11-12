// uilistboxentry.cpp - UIListBoxEntry icons (original: C:\aqua\src\UI\UIListBox.cpp).
// #line directives reproduce the original __LINE__ values and file name passed to the logger.
#include <string.h>
#include <algorithm>
#include "BFLog.h"
#include "gximage.h"
#include "gxvidman.h"
#include "uilistbox.h"
#include "uilistboxentry.h"

// 0x417E94
// name: string (the BFLog text "UIListBoxEntry::setNormalIcon() - Acquiring %s")
void UIListBoxEntry::setNormalIcon(const char* name)
{
    int height = 0;
    if (name != 0 && *name != 0)
    {
        int length = strlen(name);
        if (length > 4 && _stricmp(".tga", name + length - 4) == 0)
        {
            m_normalName.f4b1e62();
            GXImage image;
#line 88 "C:\\aqua\\src\\UI\\UIListBox.cpp"
            BFLog(BFLOG_ARGS(BFLOG_NOTE), "UIListBoxEntry::setNormalIcon() - Acquiring %s", name);
            image.vf1(name);
            if (image.isValid())
            {
                GXVidMan* vidMan = g_gxVidMan;
                m_normalCanvas = vidMan->createSurface(image.getWidth(), image.getHeight());
                image.vf10(&m_normalCanvas, 0, 0);
                m_normalCanvas.setColorKey(0, 0);
                height = image.getHeight();
            }
        }
        else
        {
            m_normalCanvas.releaseSurface();
            if (f4176ce(&m_normalFrame, &m_normalName, name))
                height = m_normalFrame->bottom - m_normalFrame->top;
        }
    }
    height = _STL::max(height, m_owner->getUnk390());
    m_unk24 = _STL::max(m_unk24, height);
    f417c8c();
}

// 0x47098B
// name: string (the BFLog text "UIListBoxEntry::setSelectedIcon() - Acquiring %s")
void UIListBoxEntry::setSelectedIcon(const char* name)
{
    int height = 0;
    if (name != 0 && *name != 0)
    {
        int length = strlen(name);
        if (length > 4 && _stricmp(".tga", name + length - 4) == 0)
        {
            m_selectedName.f4b1e62();
            GXImage image;
#line 124 "C:\\aqua\\src\\UI\\UIListBox.cpp"
            BFLog(BFLOG_ARGS(BFLOG_NOTE), "UIListBoxEntry::setSelectedIcon() - Acquiring %s", name);
            image.vf1(name);
            if (image.isValid())
            {
                GXVidMan* vidMan = g_gxVidMan;
                m_selectedCanvas = vidMan->createSurface(image.getWidth(), image.getHeight());
                image.vf10(&m_selectedCanvas, 0, 0);
                m_selectedCanvas.setColorKey(0, 0);
                height = image.getHeight();
            }
        }
        else
        {
            m_selectedCanvas.releaseSurface();
            if (f4176ce(&m_selectedFrame, &m_selectedName, name))
                height = m_selectedFrame->bottom - m_selectedFrame->top;
        }
    }
    height = _STL::max(height, m_owner->getUnk390());
    m_unk24 = _STL::max(m_unk24, height);
    f417c8c();
}

// 0x474C26
// name: string (the BFLog text "UIListBoxEntry::setGrayedIcon() - Acquiring %s")
void UIListBoxEntry::setGrayedIcon(const char* name)
{
    int height = 0;
    if (name != 0 && *name != 0)
    {
        int length = strlen(name);
        if (length > 4 && _stricmp(".tga", name + length - 4) == 0)
        {
            m_grayedName.f4b1e62();
            GXImage image;
#line 160 "C:\\aqua\\src\\UI\\UIListBox.cpp"
            BFLog(BFLOG_ARGS(BFLOG_NOTE), "UIListBoxEntry::setGrayedIcon() - Acquiring %s", name);
            image.vf1(name);
            if (image.isValid())
            {
                GXVidMan* vidMan = g_gxVidMan;
                m_grayedCanvas = vidMan->createSurface(image.getWidth(), image.getHeight());
                image.vf10(&m_grayedCanvas, 0, 0);
                m_grayedCanvas.setColorKey(0, 0);
                height = image.getHeight();
            }
        }
        else
        {
            m_grayedCanvas.releaseSurface();
            if (f4176ce(&m_grayedFrame, &m_grayedName, name))
                height = m_grayedFrame->bottom - m_grayedFrame->top;
        }
    }
    height = _STL::max(height, m_owner->getUnk390());
    m_unk24 = _STL::max(m_unk24, height);
    f417c8c();
}
