// BFLog.h - Blue Fang logging (zoo.ini [debug] logCutoff / deltaLog*).
#ifndef BFLOG_H
#define BFLOG_H

#include <windows.h>
#include <stdarg.h>

// log levels (names from BFLogLevelName)
enum
{
    BFLOG_TRACE = 3,
    BFLOG_INFO  = 6,
    BFLOG_NOTE  = 9,
    BFLOG_ERROR = 12,
    BFLOG_FATAL = 15
};

extern int  g_bfLogCutoff;          // 0x63804C  (zoo.ini [debug] logCutoff)
extern int  g_bfLogDelta;           // 0x638054  (passed as "delta" by plain log calls)
extern bool g_bfLogToDebugger;      // 0x643E44
extern bool g_bfLogToFile;          // 0x643E48
extern bool g_bfLogMessageBox;      // 0x643E4A

void BFLog(const char* file, int line, int hrLevel, int level, int delta, HRESULT hr, bool hasHr,
           const char* fmt, ...);
void BFLogV(const char* file, int line, int level, bool hasHr, int delta, HRESULT hr,
            const char* fmt, va_list args);

void BFLogHR(const char* file, int line, int failLevel, int okLevel, HRESULT hr, const char* fmt, ...);

// Argument helpers (VC6 has no variadic macros):
//   BFLog(BFLOG_ARGS(BFLOG_ERROR), "fmt", ...);
//   BFLogHR(BFLOG_HR_ARGS(hr), "fmt", ...);      - ERROR if FAILED(hr), TRACE otherwise
#define BFLOG_ARGS(level)  __FILE__, __LINE__, level, level, g_bfLogDelta, 0, false
#define BFLOG_HR_ARGS(hr)  __FILE__, __LINE__, BFLOG_ERROR, BFLOG_TRACE, hr

#endif
