// BFLog.cpp - Blue Fang logging core.
// Original functions (zoo.exe): see Notes\zoo.map, "BFLog" entries.

#include "BFLog.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// ---- outside this file (addresses in the original) ----
struct BFApp;
BFApp* BFGetApp();                                       // 0x4010C7
const char* BFDXErrorString(HRESULT hr);                 // 0x603505 (DirectX error table)
void BFLogWriteFile(const char* text, unsigned int len); // 0x6033BA
void BFLogDebugString(const char* text);                 // 0x52B8C4

struct BFApp
{
    char pad[0x4C4];
    HWND m_hwnd;
};

static char s_line[1024];      // 0x64567C: the line being built
static char s_tmp[1024];       // 0x645A7C: scratch for one piece

// 0x52BA65
const char* BFLogLevelName(int level)
{
    switch (level)
    {
    case BFLOG_TRACE: return "TRACE";
    case BFLOG_INFO:  return "INFO ";
    case BFLOG_NOTE:  return "NOTE ";
    case BFLOG_ERROR: return "ERROR";
    case BFLOG_FATAL: return "FATAL";
    }
    return "BFLOG";
}

// 0x52BA7B
void BFLogHeader(int level, const char* file, int line)
{
    if (level < 100)
    {
        sprintf(s_tmp, "%s(%d) : ", file, line);
        strcat(s_line, s_tmp);
    }
    sprintf(s_tmp, "%s : ", BFLogLevelName(level));
    strcat(s_line, s_tmp);
}

// 0x52B9A2
void BFLogMessage(const char* fmt, va_list args)
{
    _vsnprintf(s_tmp, sizeof(s_tmp) - 1, fmt, args);
    strcat(s_tmp, "\n");
    strcat(s_line, s_tmp);
}

// 0x52B94A  OPEN: the original saves ebx/esi/edi before the hasHr test; ours saves them inside the if.
//            Tried: function-scope locals, early return, both, a copied hr - no change.
void BFLogHResult(bool hasHr, HRESULT hr)
{
    if (hasHr)
    {
        const char* text;
        sprintf(s_tmp, "  HRESULT [0x%8x][%d]: ", hr, hr & 0xFFFF);
        strcat(s_line, s_tmp);
        const char* dx = BFDXErrorString(hr);
        if (dx)
        {
            strcat(s_line, dx);
            text = "\n";
        }
        else
        {
            text = FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM, 0, hr, 0, s_tmp, sizeof(s_tmp), 0)
                 ? s_tmp : "Unknown\n";
        }
        strcat(s_line, text);
    }
}

// 0x401363  The original's "push s_line; sub esp,4; ...; add esp,8" is BFLogDebugString inlined by
//           the post-link optimizer (MATCHING_NOTES 5), so the source simply calls it.
void BFLogV(const char* file, int line, int level, bool hasHr, int delta, HRESULT hr,
            const char* fmt, va_list args)
{
    if (level - delta >= g_bfLogCutoff)
    {
        s_line[0] = 0;
        BFLogHeader(level, file, line);
        BFLogMessage(fmt, args);
        BFLogHResult(hasHr, hr);
        if (g_bfLogMessageBox && level == BFLOG_ERROR)
        {
            HWND owner = BFGetApp()->m_hwnd;
            if (MessageBoxA(owner, s_line, "Hey guys! Whatcha tryna to do?!",
                            MB_OKCANCEL | MB_ICONEXCLAMATION) == IDCANCEL)
                abort();
        }
        if (g_bfLogToFile)
            BFLogWriteFile(s_line, strlen(s_line));
        if (g_bfLogToDebugger)
            BFLogDebugString(s_line);
    }
}

// 0x52B8C4  no callers left in zoo.exe: BBT inlined every call
void BFLogDebugString(const char* text)
{
    OutputDebugStringA(text);
}

// 0x401386
void BFLog(const char* file, int line, int hrLevel, int level, int delta, HRESULT hr, bool hasHr,
           const char* fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    BFLogV(file, line, hasHr ? hrLevel : level, hasHr, delta, hr, fmt, args);
}

// 0x40514D
void BFLogHR(const char* file, int line, int failLevel, int okLevel, HRESULT hr, const char* fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    BFLogV(file, line, hr < 0 ? failLevel : okLevel, hr < 0, 0, hr, fmt, args);
}
