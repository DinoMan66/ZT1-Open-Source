@echo off
rem Starts the local model, queues pre-reading of the next targets, and runs the reader, in one go
rem (Tools\localai\watch_ai.py). Double-click it, or run it from any folder. Leave both windows open during a
rem decompilation session; close them when done. The model is only reachable from this PC (127.0.0.1).
rem The model window restarts llama-server by itself if it stops, and keeps the reason on screen and in
rem Tools\localai\out\llama-server.log / llama-stops.txt.

rem --- change these lines if your setup differs -----------------------------------------------------
set LLAMA=C:\Llama\llama-server.exe
set MODEL=mradermacher/Qwen3.5-9B-heretic-GGUF:Q4_K_M
rem context in tokens: 32768 reads about 80 KB at once; 16384 needs less video memory if the server crashes
set CTX=32768
rem ---------------------------------------------------------------------------------------------------

cd /d "%~dp0..\.."
if not exist "%LLAMA%" (
    where %LLAMA% >nul 2>nul || (
        echo Cannot find %LLAMA%. Edit the LLAMA= line in Tools\localai\start_local_ai.bat to its full path.
        pause & exit /b 1
    )
)
if not exist "Tools\localai\out" mkdir "Tools\localai\out"
start "local model (llama-server)" cmd /c call "Tools\localai\run_llama.bat"
rem pre-read the next targets (Tools\next.py) so the next session starts from short digests
py Tools\localai\preread.py
py Tools\localai\watch_ai.py --url http://127.0.0.1:8080
pause
