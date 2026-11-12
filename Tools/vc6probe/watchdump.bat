@echo off
rem Probe\weights\watchdump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb with hardware write breakpoints on the addresses listed in watch.txt (one per line,
rem at most 4; c2's heap is deterministic for the same input) and logs every write (value, source line, call stack)
rem to Results\<name>.watch.txt. Only reads the probe inputs.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo watchdump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\watchdump.cdb
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
for /f %%a in (%HERE%watch.txt) do >> "%SCRIPT%" echo ba w4 %%a ".printf \"W %%a=%%x line=%%d eip=%%x ret=%%x\\n\", poi(%%a), wo(0x107ac360), @eip, poi(@esp); k 8; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo watchdump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.watch.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
