@echo off
rem Probe\weights\bothdump.bat - run by the build (Tools\queue\cmd_<id>.bat). Compiles every Probe\weights\in\*.cpp
rem with C:\VC6SP3\Bin under cdb and logs, to Results\<name>.add.txt, every call of c2's address-mode matcher
rem FUN_10729327 (autoadd.cdb) and every address operand it builds (FUN_1071f60f / FUN_107216d8, autoam.cdb)
rem and every `x = x + rest` rewrite of FUN_1072735c (E = entry with the source tree, autorw.cdb,
rem F = tree search result, RW = rewrite).
rem Only reads the probe inputs.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo bothdump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\bothdump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x10729327 "$$>a<%HERE2%autoadd.cdb; g"
>> "%SCRIPT%" echo bp 0x1071f60f "r $t19=6; $$>a<%HERE2%autoam.cdb; g"
>> "%SCRIPT%" echo bp 0x1072735c "$$>a<%HERE2%autorw.cdb; g"
>> "%SCRIPT%" echo bp 0x10727497 ".printf \"F=%%d\\n\", @eax; g"
>> "%SCRIPT%" echo bp 0x107274c6 ".printf \"RW line=%%d dest=%%x\\n\", wo(0x107ac360), poi(poi(poi(@esp)+14)+1c); g"
>> "%SCRIPT%" echo bp 0x107216d8 "r $t19=5; $$>a<%HERE2%autoam.cdb; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo bothdump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.add.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
