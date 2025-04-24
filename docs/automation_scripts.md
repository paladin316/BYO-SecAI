# 🛠️ Automation Scripts – `scripts/` Folder

This page documents each automation script included in the `scripts/` directory of the BYO-SecAI project.

---

## 📜 `install_byo_secai.ps1` – PowerShell Setup Script

This script automates the entire setup of BYO-SecAI on a Windows system. It:

- Verifies Python 3.10, Docker Desktop, and Ollama are installed
- Creates a Python virtual environment (`jarvis_env`)
- Installs required Python modules via `requirements.txt`
- Starts the `phi`, `mistral`, and `llama3` LLMs using Ollama
- Launches OpenWebUI via Docker
- Logs output and errors during setup

Run it from PowerShell:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install_byo_secai.ps1
```

---

## 🤖 `jarvis_no_voice.py` – Headless Assistant CLI

A simple Python script to interact with your local LLM via OpenWebUI API.

- Sends a hardcoded test query about MITRE T1059
- Returns model output to the terminal

You can modify it to support dynamic prompts or embed it into automation pipelines.

```bash
python scripts/jarvis_no_voice.py
```

---

## 🪟 `run_every_boot.bat` – Windows Startup Launcher

This batch file is designed to be triggered on system boot. It:

- Activates the Python virtual environment
- Prunes exited Docker containers (cleanup)
- Starts `phi`, `mistral`, and `llama3` via Ollama
- Brings up OpenWebUI in the background
- Logs all actions to `logs/startup_log.txt`

You can manually run it or hook it to Task Scheduler.

---

## ⏰ `byo_secai_autostart.xml` – Task Scheduler Definition

This XML file defines a Windows Task Scheduler job that runs `run_every_boot.bat` on user login.

To use it:
1. Open **Task Scheduler**
2. Click **Import Task**
3. Select `scripts/byo_secai_autostart.xml`
4. Update the `Command` path to your actual `run_every_boot.bat` file location

---

These scripts make it easy to install, run, and maintain your local SecAI assistant automatically and securely.