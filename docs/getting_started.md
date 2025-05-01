# Getting Started with BYO-SecAI

Welcome to **BYO-SecAI** — your own private AI assistant for cybersecurity research, threat hunting, detection engineering, and intel analysis.

This guide walks you through setting up the local BYO-SecAI environment using open-source LLM runtimes like **Ollama**, enhanced with **plugin orchestration**, **RAG capability**, and **enterprise-grade command modules**.

---

## 🧱 Prerequisites

- Windows 10 or 11 (64-bit)
- 16 GB RAM minimum (32 GB recommended)
- Python 3.10 (not 3.12+)
- Docker Desktop with WSL2 backend enabled
- Ollama (for local LLM runtime)
- (Optional) NVIDIA GPU with CUDA

---

## 📦 Step 1: Install Required Software

### Python 3.10
[Download Python 3.10.13](https://www.python.org/downloads/release/python-31013/)  
✔️ Select **Add Python to PATH** during installation.

---

### Docker Desktop
[Download Docker Desktop](https://www.docker.com/products/docker-desktop)  
Enable the **WSL2 backend** during install. Reboot if prompted.

---

### Ollama
[Install Ollama](https://ollama.com/download)  
Test by running:
```bash
ollama run phi
```

---

## 🌐 Step 2: (Optional) OpenWebUI GUI

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
docker-compose up -d
```

Browse to: [http://localhost:3000](http://localhost:3000)

---

## 🤖 Step 3: Prepare Your Assistant

```powershell
cd scripts/
python -m venv jarvis_env
.\jarvis_env\Scripts\activate
pip install -r requirements.txt
```

---

## 🧠 Step 4: Launch the AI Assistant

```powershell
.\Launch_LLM-Powered_RAG_Assistant.bat
```

This script:
- Activates your Python virtual environment
- Starts `llm_orchestrator_with_plugins.py` with enterprise command modules
- Initializes plugins, RAG modules, and intellisense
- Writes all outputs to `evidence/` for audit-ready records

---

## 💻 Available Commands

Once launched, you can invoke the following modules via the interactive CLI:

| Command               | Description                                              |
|-----------------------|----------------------------------------------------------|
| **threat_ops_qa**     | ThreatOps Q&A Assistant (Mistral-based)                  |
| **detection_studio**  | Detection Logic Studio (CodeLlama-based)                 |
| **ttp_mapper**        | MITRE TTP Mapper (Phi-based)                             |
| **codegen_assistant** | CodeGen Assistant for YARA & Scripts (CodeLlama-based)   |
| **playbook_designer** | Playbook Designer for IR SOPs (Llama2-based)             |
| **rag_explorer**      | RAG Explorer – Query Uploaded Data Only (Llama3-based)   |
| **unified_analyst**   | Unified Analyst – General LLM + RAG (Llama3-based)       |
| **plugin_ioc**        | Scan an IOC using enabled plugins                        |
| **help**              | Show this help menu                                      |
| **exit**              | Exit the interactive session                             |

---

## 🔌 RAG – Retrieval-Augmented Generation

Drop documents (PDF, CSV, TXT, MD, logs) into `data/` and ingest:
```powershell
python scripts/rag_ingest_and_query.py --ingest data/
```

Query your knowledge base:
```powershell
python scripts/rag_ingest_and_query.py --query "Show suspicious logins"
```

Or launch the optional Streamlit dashboard:
```powershell
streamlit run scripts/streamlit_rag_ui.py
```

---

## ✅ Best Practices

- Restrict network access to `localhost` only
- Run in offline mode when possible
- Validate all FAISS indexes originate from trusted sources

---

## 📚 Additional Documentation

- [`model_guide.md`](model_guide.md) – Prompt examples & tuning tips
- [`use_cases.md`](use_cases.md) – Sample workflows
- [`security.md`](security.md) – Hardening & firewall rules
- [`automation_scripts.md`](automation_scripts.md) – Startup & scheduling
- [`CHANGELOG.md`](CHANGELOG.md) – Release history

---

Made with 🛡️ by **Paladin316** and 🤖 powered by **Aegis (My AI Assistant)**

