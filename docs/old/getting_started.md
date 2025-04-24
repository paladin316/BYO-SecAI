
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

## 🤖 Step 3: Connect OpenWebUI to Ollama

- Open OpenWebUI
- Go to **Settings → Models**
- Provider: **Ollama**
- API URL: `http://host.docker.internal:11434`
- Model: `phi`, `mistral`, or your preferred Ollama model

---

## 🧠 Step 4: Run the Assistant Script

Navigate to the `scripts` directory and run:

```bash
python jarvis_no_voice.py
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

## ✅ Next Steps

- Explore model strengths in [`model_guide.md`](model_guide.md)
- Automate assistant startup with [`autostart.md`](autostart.md)
- Review setup requirements in [`requirements.md`](requirements.md)

---

Made with 🛡️ by Paladin316 and 🤖 powered by Aegis (My AI Assistant)
