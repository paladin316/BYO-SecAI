@echo off
   title Advanced RAG Assistant

   call jarvis_env\Scripts\activate

   set "LLM_ORCHESTRATOR_PATH="C:\Users\user\projects\GitHub\BYO-SecAI-Final-Package\scripts\llm_orchestrator_with_plugins.py""

   python "%LLM_ORCHESTRATOR_PATH%"
   pause