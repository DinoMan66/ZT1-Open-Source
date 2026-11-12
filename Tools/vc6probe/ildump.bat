@echo off
rem Probe\weights\ildump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb and prints, for every function, the intermediate code exactly as c2 has read
rem it from the front end (after FUN_1071b973, autoil.cdb) to Results\<name>.il.txt. Only reads the probe inputs.
rem Probe\weights\ildump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo ildump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\ildump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x10768269 "$$>a<%HERE2%autoil.cdb; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo ildump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.il.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
