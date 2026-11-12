@echo off
rem Probe\weights\autodump.bat - run by the build (Tools\queue\cmd_<id>.bat) when C:\anticheat_allow_cmd.txt exists.
rem Compiles every Probe\weights\in\*.cpp with C:\VC6SP3\Bin under cdb and writes VC6's register-candidate
rem priority list to Results\<name>.weights.txt, plus one "T reg= ptr=" line per scratch-register
rem assignment of the local allocator (c2 FUN_1073356b; ptr = its round-robin index, id = temp id) and one
rem "G id= reg=" line per global register assignment (c2 FUN_107245c3), "A op= id= pref= conf=" before each local pick (autoconf.cdb)
rem (FUN_10733273) and "B reg= line=" per pick of the per-block allocator (FUN_10732fbc), "E id= reg= nb=" interference edges (autoedge.cdb), "P id= blocks=" first source line of each block of a pick (autopiece.cdb), "R" at each priority computation and "Q k= id= P= b=" per block contribution to a priority (autoprio.cdb). Only reads the probe inputs; objects go to %TEMP%.
setlocal
set HERE=%~dp0
set CDB=C:\Program Files\Debugging Tools for Windows (x86)\cdb.exe
if not exist "%CDB%" (echo autodump: cdb.exe not found & exit /b 1)
call "C:\Program Files\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" >nul
set PATH=C:\VC6SP3\Bin;%PATH%
set SCRIPT=%TEMP%\autodump.cdb
set HERE2=%HERE:\=\\%
> "%SCRIPT%" echo sxe ld:c2.dll
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo bp 0x10722463 ".printf \"R\\n\"; g"
>> "%SCRIPT%" echo bp 0x10722d4c "r $t19=1; $$>a<%HERE2%autoprio.cdb; g"
>> "%SCRIPT%" echo bp 0x10722d6b "r $t19=2; $$>a<%HERE2%autoprio.cdb; g"
>> "%SCRIPT%" echo bp 0x10722d99 "r $t19=3; $$>a<%HERE2%autoprio.cdb; g"
>> "%SCRIPT%" echo bp 0x1072450d "gu; $$>a<%HERE2%autolist.cdb; g"
>> "%SCRIPT%" echo bp 0x1073356b ".printf \"T reg=%%d ptr=%%d id=%%d line=%%d\\n\", @ecx, (poi(0x1079d710)-0x107adff4)/4, poi(@edx+1c), wo(0x107ac360); g"
>> "%SCRIPT%" echo bp 0x10733273 "$$>a<%HERE2%autoconf.cdb; g"
>> "%SCRIPT%" echo bp 0x10732fbc "gu; .printf \"B reg=%%d line=%%d\\n\", @eax, wo(0x107ac360); g"
>> "%SCRIPT%" echo bp 0x10724877 "$$>a<%HERE2%autoedge.cdb; g"
>> "%SCRIPT%" echo bp 0x107245c3 "r $t1=@ecx; r $t6=0; .if (poi(poi(@ecx+20)) != 0) { r $t6=poi(poi(poi(@ecx+20))+8) }; gu; $$>a<%HERE2%autoglob.cdb; $$>a<%HERE2%autopiece.cdb; g"
>> "%SCRIPT%" echo g
>> "%SCRIPT%" echo q
pushd "%HERE%in"
for %%f in (*.cpp) do (
  echo autodump %%f
  "%CDB%" -G -cf "%SCRIPT%" -logo "%ROOT%\Results\%%~nf.weights.txt" cl.exe /nologo /c /W3 /ML /O2 /D WIN32 /D NDEBUG /D _WINDOWS /I "%HERE%..\..\Src\include" /Fo"%TEMP%\%%~nf.obj" "%%f" >nul
)
popd
del /q "%HERE%in\*.cpp" >nul 2>&1
