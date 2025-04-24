@echo off
REM BYO-SecAI CLI Launcher for jarvis_no_voice.py
title BYO-SecAI CLI Assistant
echo Launching BYO-SecAI CLI Assistant from virtual environment...

cd /d %~dp0
call jarvis_env\Scripts\activate.bat
python scripts\jarvis_no_voice.py

pause