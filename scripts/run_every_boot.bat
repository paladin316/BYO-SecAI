@echo off
REM BYO-SecAI Auto Startup Script

REM Activate Python virtual environment
call "%~dp0..\jarvis_env\Scripts\activate.bat"

REM Run assistant script (optional)
REM python "%~dp0..\scripts\jarvis_no_voice.py"

REM Start Ollama models
start "" /min cmd /c "ollama run phi"
start "" /min cmd /c "ollama run mistral"
start "" /min cmd /c "ollama run llama3"

REM Start OpenWebUI
cd /d "%USERPROFILE%\open-webui"
start "" /min cmd /c "docker-compose up -d"