@echo off
setlocal enableextensions
title Zoo Tycoon build watcher
rem ======================================================================
rem  Zoo Tycoon build watcher - run it inside the XP VM and leave the window open.
rem  It waits for Tools\queue\request*.txt and then runs Tools\build_core.bat,
rem  so Claude can change the build steps without you restarting this window.
rem  Ctrl+C stops it.
rem ======================================================================
pushd "%~dp0.."
set ROOT=%CD%
if "%ROOT:~-1%"=="\" set ROOT=%ROOT:~0,-1%
set QUEUE=%ROOT%\Tools\queue
if not exist "%QUEUE%" mkdir "%QUEUE%"

echo Project : %ROOT%
echo Watching: %QUEUE%\request*.txt
echo (leave this window open; Ctrl+C stops it)
echo.

:loop
rem uniquely named requests (request_<id>.txt) avoid the shared folder serving a cached copy
for %%r in ("%QUEUE%\request*.txt") do call :build "%%~r"
ping -n 4 127.0.0.1 >nul
goto loop

:build
set REQ=
set /p REQ=<"%~1"
del "%~1"
echo [%date% %time%] request: %REQ%
if exist "%ROOT%\Tools\build_core.bat" (
  call "%ROOT%\Tools\build_core.bat" "%ROOT%" "%REQ%"
) else (
  echo   ERROR: %ROOT%\Tools\build_core.bat is missing
)
echo [%date% %time%] finished
echo.
goto :eof
