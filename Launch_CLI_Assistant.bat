@echo off
title BYO-SecAI CLI Assistant

echo ================================================
echo                🧠 BYO-SecAI Assistant
echo ================================================
echo.

:menu
echo Select an option:
echo [1] Ask Jarvis (LLM only)
echo [2] Ask with RAG (use your ingested documents)
set /p choice=Enter choice (1 or 2):

call jarvis_env\Scripts\activate

set "PYTHON_SCRIPT_PATH=C:\\Users\\user\\projects\\GitHub\\BYO-SecAI-Final-Package\\scripts\\rag_ingest_and_query.py"
set "JARVIS_NO_VOICE_PATH=C:\\Users\\user\\projects\\GitHub\\BYO-SecAI-Final-Package\\scripts\\jarvis_no_voice.py"
set "DATA_DIR_PATH=C:\\Users\\user\\projects\\GitHub\\BYO-SecAI-Final-Package\\data"

if "%choice%"=="1" (
    echo Launching direct assistant...
    python "%JARVIS_NO_VOICE_PATH%"
    goto end
) else if "%choice%"=="2" (
    if exist vector_index\ (
        echo ✅ Existing vector index detected.
        echo Launching RAG query...
        python "%PYTHON_SCRIPT_PATH%" --query ""
    ) else (
        echo 🚧 No vector index found. Ingesting /data and launching query...
        python "%PYTHON_SCRIPT_PATH%" --ingest "%DATA_DIR_PATH%" --query ""
    )

) else (
    echo Invalid choice. Please enter 1 or 2.
    goto menu
)

:end
pause