@echo off
setlocal
rem ======================================================================
rem  Exports Ghidra's decompiled C for zoo.exe (HEADLESS mode). Run on the PC, not in the VM.
rem  Usage: double-click.  Output: decompiled\zoo.exe.c  (+ zoo.exe.log)
rem  Ghidra folder is read from Tools\ghidra_path.txt.
rem ======================================================================
set TOOLS=%~dp0
cd /d "%~dp0.."
set ROOT=%CD%
set TARGET=%ROOT%\Original\zoo.exe
if not "%~1"=="" set TARGET=%~f1
set PROJ=%ROOT%\ghidra_project
set OUT=%ROOT%\decompiled
set /p GHIDRA=<"%TOOLS%ghidra_path.txt"
if not exist "%GHIDRA%\support\analyzeHeadless.bat" (
  echo ERROR: Ghidra not found at "%GHIDRA%" - fix Tools\ghidra_path.txt
  pause
  exit /b 1
)
if not exist "%PROJ%" mkdir "%PROJ%"
if not exist "%OUT%"  mkdir "%OUT%"
echo Exporting %TARGET% - this takes a while for a 2 MB exe.
call "%GHIDRA%\support\analyzeHeadless.bat" "%PROJ%" ZooTycoon -import "%TARGET%" -overwrite -scriptPath "%TOOLS%ghidra" -postScript ExportDecompiled.java "%OUT%" > "%OUT%\zoo.exe.log" 2>&1
echo.
echo Done. Output folder: %OUT%
dir "%OUT%"
pause
