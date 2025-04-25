@echo off
title Launch BYO-SecAI CLI Assistant
echo ================================================
echo         🧠 Launching BYO-SecAI Assistant
echo ================================================
echo.

echo Select an option:
echo [1] Ask Jarvis (LLM only)
echo [2] Ask with RAG (use your ingested documents)
set /p choice=Enter choice (1 or 2): 

call jarvis_env\Scripts\activate

if "%choice%"=="1" (
    echo Launching direct assistant...
    python scripts\jarvis_no_voice.py
) else if "%choice%"=="2" (
    if exist vector_index\ ( 
        echo ✅ Existing vector index detected.
    ) else (
        echo 🚧 No vector index found. Ingesting /data...
        python scripts\rag_ingest_and_query.py --ingest data
    )

    echo.
    echo ============================================
    echo 🔍 RAG Ready! Now ask a question to Jarvis:
    echo ============================================
    python scriptsag_ingest_and_query.py --query " " 
) else (
    echo Invalid choice. Please run the script again.
)

pause