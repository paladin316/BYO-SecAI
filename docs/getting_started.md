# Getting Started with BYO-SecAI

Welcome to **BYO-SecAI** — your own private AI assistant for cybersecurity research, threat hunting, detection engineering, and intel analysis.

This guide walks you through setting up the local BYO-SecAI environment using open-source LLM runtimes like **Ollama**, enhanced with **plugin orchestration**, **RAG capability**, and **evidence-driven workflows**.

---

## 🧱 Prerequisites

- Windows 10 or 11 (64-bit)
- 16 GB RAM minimum (32 GB recommended)
- Python 3.10 (not 3.12+)
- Docker Desktop with WSL2 backend enabled
- Ollama (for local LLM runtime)
- (Optional) NVIDIA GPU with CUDA

---

## 📦 Step 1: Install Required Software

### Python 3.10
[Download Python 3.10.13](https://www.python.org/downloads/release/python-31013/)  
✔️ Select “Add Python to PATH” during installation.

---

### Docker Desktop
[Download Docker Desktop](https://www.docker.com/products/docker-desktop)  
Enable the **WSL2 backend** during install. Reboot when prompted.

---

### Ollama
[Install Ollama](https://ollama.com/download)  
Test by running:
```bash
ollama run phi
```

---

## 🌐 Step 2: Setup OpenWebUI (Optional GUI)

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
docker-compose up -d
```

Browse to: [http://localhost:3000](http://localhost:3000)

---

## 🤖 Step 3: Prepare Your Assistant

Navigate to the `scripts/` folder and set up your environment:

```powershell
python -m venv jarvis_env
.\jarvis_env\Scriptsctivate
pip install -r requirements.txt
```

---

## 🧠 Step 4: Launch the AI Assistant

Use the new orchestrator to start your assistant with plugin and RAG support:

```powershell
.\Launch_LLM-Powered_RAG_Assistant.bat
```

This script:
- Activates your Python virtual environment
- Initializes `llm_orchestrator_with_plugins.py`
- Loads all plugins and RAG modules
- Creates output in `investigation_evidence/`
- Offers an interactive CLI with intellisense tab-completion

---

## 🔌 Supported Plugins

Out-of-the-box support for:
- 🦠 VirusTotal
- 🕵️ AbuseIPDB
- 🌐 urlscan.io
- ⚙️ Expandable plugin system (see `scripts/plugins/`)

Run `plugin_ioc <ip or domain>` to test.

---

## 🧠 Retrieval-Augmented Generation (RAG)

Query your own data files using RAG!  
Drop files into the `data/` folder and use:

```powershell
python scripts/rag_ingest_and_query.py --ingest data/
python scripts/rag_ingest_and_query.py --query "Show suspicious logins"
```

Use the Streamlit UI with:
```powershell
streamlit run scripts/streamlit_rag_ui.py
```

---

## 🧪 Assistant Features

- Natural language command interface
- Plugin-based CTI lookups
- Custom script execution (bash, PowerShell, Python)
- RAG over `.pdf`, `.csv`, `.md`, `.log`
- Evidence export to `investigation_evidence/`
- CLI auto-completion for fast workflows

---

## ✅ Best Practices

- Keep traffic to `localhost` only
- Block network access to OpenWebUI/Ollama ports
- Use offline mode when possible
- Avoid loading untrusted `.pkl` files in FAISS

---

## 📚 More Resources

- [`model_guide.md`](model_guide.md) – LLM tips and prompt examples  
- [`use_cases.md`](use_cases.md) – CLI assistant workflows  
- [`security.md`](security.md) – Hardening tips  
- [`automation_scripts.md`](automation_scripts.md) – Startup scripts  
- [`CHANGELOG.md`](CHANGELOG.md) – See what’s new  

---

Made with 🛡️ by **Paladin316** and 🤖 powered by **Aegis (My AI Assistant)**
