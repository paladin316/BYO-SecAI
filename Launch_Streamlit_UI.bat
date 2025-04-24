@echo off
REM BYO-SecAI Streamlit Launcher with venv activation
title BYO-SecAI RAG UI
echo Launching Streamlit RAG UI from virtual environment...

cd /d %~dp0
call jarvis_env\Scripts\activate.bat
python -m streamlit run scripts\streamlit_rag_ui.py --server.runOnSave=false

pause