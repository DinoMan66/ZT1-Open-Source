@echo off
rem Probe\weights\deldump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb and logs, from the start of c2's `x = x + rest` pass (FUN_1072626e) on, every
rem tuple that is unlinked and freed (FUN_1070179c, autodel.cdb) with its caller, plus "PRI" at each register
rem priority computation (FUN_10722463), to Results\<name>.del.txt. Only reads the probe inputs.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo deldump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\deldump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo r $t18 = 0
>> "%SCRIPT%" echo bp 0x1072626e "r $t18 = 1; .printf \"PASS rewrite\\n\"; g"
>> "%SCRIPT%" echo bp 0x10722463 "r $t18 = 0; .printf \"PRI\\n\"; g"
>> "%SCRIPT%" echo bp 0x1070179c ".if (@$t18 == 1) { $$>a<%HERE2%autodel.cdb }; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo deldump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.del.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
