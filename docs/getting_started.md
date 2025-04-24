# Getting Started with BYO-SecAI

Welcome to **BYO-SecAI** — your own private AI assistant for cybersecurity research.

This guide will walk you through setting up the local environment required to run your assistant using open-source tools like **Ollama** and **OpenWebUI**.

---

## 🧱 Prerequisites

- Windows 10 or 11 (64-bit)
- 16 GB RAM minimum (32 GB recommended)
- Python 3.10 (not 3.12+)
- Docker Desktop with WSL2 backend enabled
- Ollama (for running LLMs locally)

(Optional: NVIDIA GPU with CUDA for improved performance)

---

## 📦 Step 1: Install Required Software

### Python 3.10
[Download Python 3.10.13](https://www.python.org/downloads/release/python-31013/)

✔️ Check “Add Python to PATH” during installation.

---

### Docker Desktop
[Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

- Enable the **WSL2 backend** during installation
- Reboot after install if prompted

---

### Ollama (LLM Runtime)
[Install Ollama](https://ollama.com/download)

Launch a model to test it:
```bash
ollama run phi
```

---

## 🌐 Step 2: Setup OpenWebUI

Clone and run the UI with Docker:
```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
docker-compose up -d
```

Access it at: [http://localhost:3000](http://localhost:3000)

---

## 🤖 Step 3: Setup the Assistant Script

Navigate to your `scripts/` folder and create a Python virtual environment:

```powershell
python -m venv jarvis_env
.\jarvis_env\Scriptsctivate
```

Install required Python packages:

```powershell
pip install -r requirements.txt
```

---

## 🧠 Step 4: Run the Assistant Script

Still inside the virtual environment, run:

```powershell
python scripts/jarvis_no_voice.py
```

This script lets you ask questions to your model via API:
- Threat hunting questions
- MITRE ATT&CK queries
- Detection strategy prompts

---

## 🔐 Security Best Practices

- Keep all traffic on `localhost`
- Block external access via firewall
- Use Ollama and OpenWebUI in **offline mode** when possible

See [`security.md`](security.md) for more hardening steps.

---

## 🔁 Automation Scripts

For optional startup automation and task scheduling, see:  
[`automation_scripts.md`](automation_scripts.md)

---

## ✅ Next Steps

- Explore model strengths in [`model_guide.md`](model_guide.md)
- Automate assistant startup with [`autostart.md`](autostart.md)
- Review setup requirements in [`requirements.md`](requirements.md)

---

Made with 🛡️ by Paladin316 and 🤖 powered by Aegis (My AI Assistant)

---

## 🧠 Retrieval-Augmented Generation (RAG)

BYO-SecAI supports Retrieval-Augmented Generation (RAG) to let you query your own files — such as logs, PDFs, CSVs, and Markdown — using a vector store (FAISS) and local embedding model (`all-MiniLM-L6-v2`).

### How it works
1. You drop files into the `data/` folder.
2. Text is split, embedded, and indexed to `vector_index/`.
3. You can query your documents with natural language questions.
4. RAG responses include the top matching document chunks.

---

## 🛠️ RAG Tools and Utilities

### 🔍 `scripts/check_dependencies.py`
Check which Python modules are missing for RAG:

```bash
python scripts/check_dependencies.py
```

---

### 🔧 `scripts/install_dependencies.py`
Auto-installs all Python dependencies (including FAISS, LangChain, HuggingFace):

```bash
python scripts/install_dependencies.py
```

---

### 📁 `scripts/rag_ingest_and_query.py`
- Ingest your own files into FAISS:
```bash
python scripts/rag_ingest_and_query.py --ingest data/
```

- Ask a question (after ingesting):
```bash
python scripts/rag_ingest_and_query.py --query "What logs indicate credential access?"
```

- Optional logging:
```bash
python scripts/rag_ingest_and_query.py --query "MITRE T1059" --logfile logs/query.log
```

---

### 🧪 `scripts/rag_safety_checklist.py`
Run a quick health and security check:
- Ensures `vector_index/` exists
- Confirms safe deserialization is enabled
- Checks that logs are being generated

```bash
python scripts/rag_safety_checklist.py
```

---

All logs are written to `logs/`. Your vector index is stored in `vector_index/`.
---

## 🖥️ Streamlit RAG UI (Optional)

If you prefer a web interface instead of the CLI, BYO-SecAI includes a Streamlit dashboard for document-based querying.

### Launch the Streamlit App:

```bash
streamlit run scripts/streamlit_rag_ui.py
```

Open your browser and go to [http://localhost:8501](http://localhost:8501)

### What You Can Do:

- 🔍 Ask natural language questions about your ingested files
- 📁 Upload and index `.pdf`, `.csv`, `.log`, `.txt`, or `.md` files
- 📌 Get back the top matching documents with relevance context

All documents are stored locally and never leave your machine.

---

## 🛠️ Patch Streamlit Config (Prevent Reload Errors)

To prevent Streamlit errors related to `torch.classes` and FAISS, run this script once:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/patch_streamlit_config.ps1
```

This script will:
- Create or update your Streamlit config file at `~\.streamlit\config.toml`
- Disable file watching and auto-reloading
- Prevent PyTorch/FAISS crashes due to `torch.classes`

✅ Recommended for all Windows setups using the Streamlit UI.