
# Auto-Start Guide – BYO-SecAI

This guide helps you automate the startup of your local AI assistant (LLM, UI, and assistant script) after rebooting your system.

---

## 1. Enable Docker Desktop on Login

- Open Docker Desktop
- Go to **Settings → General**
- ✅ Check: **Start Docker Desktop when you log in**

---

## 2. Auto-Start OpenWebUI Docker Container

Update the container to restart automatically:

```bash
docker update --restart unless-stopped open-webui
```

Or add this to your `docker-compose.yml`:

```yaml
restart: unless-stopped
```

---

## 3. Automatically Launch Your Ollama Model

Create a `.bat` script:

**File: `start_ollama.bat`**

```bat
@echo off
start "" "C:\Users\YourName\AppData\Local\Programs\Ollama\ollama.exe" run phi
```

Place this file in:
- `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`  
(Shortcut: Run → `shell:startup`)

Or use Task Scheduler to launch at login:
- Program: `ollama.exe`
- Arguments: `run phi`
- Set to run with highest privileges

---

## 4. (Optional) Start the Assistant Script Automatically

Create a shortcut or `.bat` script:

```bat
@echo off
cd C:\Users\YourName\projects\BYO-SecAI\scripts
call ..\jarvis_env\Scripts\activate.bat
python jarvis_no_voice.py
```

Add it to:
- Startup folder (`shell:startup`)
- Or use Task Scheduler (Log on trigger)

---

## Result

Once set up:
- Docker + OpenWebUI auto-starts
- Ollama model launches in background
- Your assistant script starts listening immediately
