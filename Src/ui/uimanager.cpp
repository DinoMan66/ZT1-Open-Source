// uimanager.cpp - UIManager (g_uiManager, 0x638DE0).
#include "uimanager.h"
#include "uicontrol.h"

// 0x44252D (name: MATCHING_NOTES 49). Makes `control` the focus control unless it is
// already the focus or one of the two controls the manager keeps in +0x08 / +0x0C.
void UIManager::setFocus(UIControl* control)
{
    if (control == m_unk0C || control == m_unk08 || control == m_focus)
        return;
    if (m_focus != 0)
        m_focus->vslot23();
    m_focus = control;
    if (control != 0)
        control->vslot22();
}

// 0x418F2F: sets the default cursor when the two cursor slots are equal
void UIManager::f418f2f()
{
    if (m_unk50 == m_unk54)
        setCursor(0, true);
}

// 0x418F43: applies the cursor in slot +0x54
void UIManager::f418f43()
{
    setCursor(m_unk54, true);
}

// 0x4D5BEA: applies the focus control's cursor
void UIManager::f4d5bea()
{
    if (m_focus)
        setCursor(m_focus->m_cursor, true);
}

// 0x4E0B8A: called by the UIControl destructor so the manager keeps no pointer to a deleted control
void UIManager::f4e0b8a(UIControl* control)
{
    if (control != 0)
    {
        if (control == m_unk08)
            m_unk08 = 0;
        if (control == m_focus)
            m_focus = 0;
        if (control == m_unk14)
            m_unk14 = 0;
        if (control == m_unk18)
            m_unk18 = 0;
    }
}
