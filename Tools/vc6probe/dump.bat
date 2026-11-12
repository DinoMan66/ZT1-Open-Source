@echo off
rem Probe\weights\dump.bat - run INSIDE the VM by hand. Not part of the build.
rem Compiles every .cpp in this folder with the game's compiler (C:\VC6SP3\Bin) under the cdb debugger
rem and logs VC6's register-allocation priority list (c2.dll) to <name>.weights.txt next to it.
rem Needs: Debugging Tools for Windows (x86), cdb.exe at the path below.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (
  echo cdb.exe not found at "%CDB%" - edit the CDB line in this file.
  pause
  exit /b 1
)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
cd /d "%HERE%"
for %%f in (*.cpp) do (
  echo dumping %%f
  "%CDB%" -G -cf "%HERE%weights.cdb" -logo "%HERE%%%~nf.weights.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f"
)
echo done - the .weights.txt files are in %HERE%
pause
