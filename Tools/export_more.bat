@echo off
setlocal
rem ======================================================================
rem  Second Ghidra pass (run on the PC after export_decompiled.bat): creates the functions
rem  Ghidra missed (virtual methods etc., from Notes\inventory.csv) in the existing project
rem  and re-exports decompiled\zoo.exe.c with all of them. No re-import, no full re-analysis.
rem ======================================================================
set TOOLS=%~dp0
cd /d "%~dp0.."
set ROOT=%CD%
set PROJ=%ROOT%\ghidra_project
set OUT=%ROOT%\decompiled
set /p GHIDRA=<"%TOOLS%ghidra_path.txt"
if not exist "%PROJ%\ZooTycoon.gpr" (
  echo ERROR: run Tools\export_decompiled.bat first
  pause
  exit /b 1
)
echo Creating missing functions and re-exporting - this takes a while.
call "%GHIDRA%\support\analyzeHeadless.bat" "%PROJ%" ZooTycoon -process zoo.exe -scriptPath "%TOOLS%ghidra" -postScript CreateFunctions.java "%ROOT%\Notes\inventory.csv" -postScript ExportDecompiled.java "%OUT%" > "%OUT%\zoo.exe.more.log" 2>&1
findstr /c:"CreateFunctions:" /c:"ExportDecompiled:" "%OUT%\zoo.exe.more.log"
echo.
echo Done. Output: %OUT%\zoo.exe.c
pause
