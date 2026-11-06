@echo off
rem ======================================================================
rem  Called by watch.bat:  build_core.bat <project root> <request id>
rem  Compiles every .cpp in Src\<folder>\ with Visual C++ 6.0 and writes Results\.
rem  Claude may update this file; watch.bat never needs restarting.
rem
rem  Compiler choice (first one found):
rem    C:\VC6SP3\Bin\cl.exe   - the SP3 compiler zoo.exe was built with (build 8447)
rem    VC98\Bin\cl.exe        - whatever Visual Studio 6 has installed (SP6 = build 8804)
rem  Optional 4th word of the request = another compiler folder name under C:\ (e.g. VC6SP4)
rem ======================================================================
setlocal enableextensions
set ROOT=%~1
set REQ=%~2
set OUT=%ROOT%\Results
rem optional 3rd word of the request = build only that Src\<folder>
set ONLY=
for /f "tokens=3" %%a in ("%REQ%") do set ONLY=%%a
if /i "%ONLY%"=="all" set ONLY=
set ALT=
for /f "tokens=4" %%a in ("%REQ%") do set ALT=%%a
set WORK=%TEMP%\ztwork

set VCVARS=C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT
rem Flags so far: release build, static single-threaded CRT (libc.lib, per the Rich header),
rem no C++ exceptions or RTTI. Refine per folder with Src\<folder>\flags.txt or per file with <file>.cpp.flags
set FLAGS=/nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS

if not exist "%OUT%" mkdir "%OUT%"
del /q "%OUT%\*.txt" >nul 2>&1
del /q "%OUT%\*.obj" >nul 2>&1
del /q "%OUT%\*.rel" >nul 2>&1

if not exist "%VCVARS%" (
  > "%OUT%\DONE.txt" echo %REQ% ERROR VCVARS32.BAT not found
  echo   ERROR: Visual C++ 6 not found
  goto :eof
)
call "%VCVARS%" >nul
rem optional commands from Claude (Tools\queue\cmd_<id>.bat) run first, so they can install a compiler; output in Results\cmd.txt
for %%c in ("%ROOT%\Tools\queue\cmd_*.bat") do call :runcmd "%%~c"
set CLDIR=
if exist "C:\VC6SP3\Bin\cl.exe" set CLDIR=C:\VC6SP3\Bin
if defined ALT if exist "C:\%ALT%\Bin\cl.exe" set CLDIR=C:\%ALT%\Bin
if defined CLDIR set PATH=%CLDIR%;%PATH%
> "%OUT%\COMPILER.txt" echo compiler folder: [%CLDIR%] (empty = VC98\Bin)
cl >> "%OUT%\COMPILER.txt" 2>&1

rem give the shared folder a moment: files written just before the request can still be served stale
ping -n 6 127.0.0.1 >nul
if exist "%WORK%" rd /s /q "%WORK%"
mkdir "%WORK%"
xcopy /E /I /Y /Q "%ROOT%\Src\*" "%WORK%\" >nul
del /q "%WORK%\*.h" >nul 2>&1

for /d %%D in ("%WORK%\*") do if /i not "%%~nxD"=="include" call :dir "%%~nxD"
del /q /s "%ROOT%\Src\Var*.cpp" >nul 2>&1
del /q /s "%ROOT%\Src\Var*.flags" >nul 2>&1
> "%OUT%\DONE.txt" echo %REQ% OK
goto :eof

:dir
if defined ONLY if /i not "%~1"=="%ONLY%" goto :eof
pushd "%WORK%\%~1"
for %%f in (*.cpp *.c) do call :one "%~1" "%%f"
popd
goto :eof

:one
set N=%~1.%~n2
set XF=
set XF2=
if exist "flags.txt" set /p XF=<"flags.txt"
if exist "%~2.flags" set /p XF2=<"%~2.flags"
echo   compiling %~1\%~2 %XF% %XF2%
> "%OUT%\%N%.compile.txt" echo extra flags: [%XF% %XF2%]
cl %FLAGS% %XF% %XF2% /I "%WORK%\include" "%~2" >> "%OUT%\%N%.compile.txt" 2>&1
if exist "%~n2.obj" (
  copy /y "%~n2.obj" "%OUT%\%N%.obj" >nul
  dumpbin /disasm "%~n2.obj" > "%OUT%\%N%.txt"
  dumpbin /relocations /symbols "%~n2.obj" > "%OUT%\%N%.rel"
) else (
  echo   FAILED: %~1\%~2
)
goto :eof

:runcmd
rem anti-cheat: a command file could replace the compiler, so only run them when the user allows it
if not exist "C:\anticheat_allow_cmd.txt" (
  >> "%OUT%\cmd.txt" echo REFUSED %~nx1 - commands are disabled by the anti-cheat. To allow them, create C:\anticheat_allow_cmd.txt INSIDE the VM yourself.
  del /q "%~1" >nul 2>&1
  goto :eof
)
call "%~1" >> "%OUT%\cmd.txt" 2>&1
del /q "%~1" >nul 2>&1
goto :eof
