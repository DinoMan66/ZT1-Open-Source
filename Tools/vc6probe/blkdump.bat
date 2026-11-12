@echo off
rem Probe\weights\blkdump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb and writes c2's basic-block order (first source line of each block) and each block's
rem successors ("S line>succ/succ,") at every depth-first walk (FUN_1070a561) to Results\<name>.blocks.txt.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo blkdump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\blkdump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x1070a561 "r $t1=poi(0x1079bc34); .if (@$t1 != 0) { .printf \"S \"; $$>a<%HERE2%autosucc.cdb }; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo blkdump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.blocks.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
