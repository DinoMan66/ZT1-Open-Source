@echo off
rem Runs llama-server and restarts it when it stops (started by start_local_ai.bat, which sets LLAMA, MODEL, CTX).
rem Close this window to stop the model for good.
:again
echo [%date% %time%] starting llama-server (context %CTX%)
"%LLAMA%" -hf %MODEL% -ngl 99 -c %CTX% --jinja --host 127.0.0.1 --port 8080 --log-file "Tools\localai\out\llama-server.log"
set CODE=%errorlevel%
echo.
echo [%date% %time%] llama-server STOPPED, exit code %CODE%. The lines above (and Tools\localai\out\llama-server.log) say why.
echo [%date% %time%] stopped, exit code %CODE%, context %CTX% >> "Tools\localai\out\llama-stops.txt"
echo Restarting in 15 seconds - close this window to stop it instead.
timeout /t 15 >nul
goto again
