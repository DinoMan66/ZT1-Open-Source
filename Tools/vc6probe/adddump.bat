@echo off
rem Probe\weights\adddump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb and logs the start tuple and its operand list at every
rem call of c2's address-mode matcher FUN_10729327 (autoadd.cdb) to Results\<name>.add.txt. Only reads the probe inputs.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo adddump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\adddump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x10729327 "$$>a<%HERE2%autoadd.cdb; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo adddump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.add.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
