@echo off
rem Probe\weights\norwdump.bat - ANALYSIS ONLY (never a build input). Run by the build (Tools\queue\cmd_<id>.bat).
rem Compiles every Probe\weights\in\*.cpp with C:\VC6SP3\Bin under cdb and, for the `x = x + rest` rewrite of
rem c2 FUN_1072735c, forces the tree search FUN_10730671 to report "not found" (eax = 0 after the call at
rem 0x10727492) whenever the cdb condition in norw.txt is true (e.g. (wo(0x107ac360) == 0n18) for a source-line
rem offset). This edits c2's intermediate code in memory to see what the code would be without that rewrite.
rem Writes the object to Results\<name>.norw.obj and a log (E/F/RW lines) to Results\<name>.norw.txt.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo norwdump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\norwdump.cdb
set HERE2=%HERE:\=\\%
set /p COND=<"%HERE%norw.txt"
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x1072735c "$$>a<%HERE2%autorw.cdb; g"
>> "%SCRIPT%" echo bp 0x10727497 ".printf \"F=%%d\\n\", @eax; .if %COND% { r eax=0; .printf \"FORCED F=0\\n\" }; g"
>> "%SCRIPT%" echo bp 0x107274c6 ".printf \"RW line=%%d\\n\", wo(0x107ac360); g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo norwdump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.norw.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%ROOT%\Results\%%~nf.norw.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
