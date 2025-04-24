
# Security & Privacy Recommendations – BYO-SecAI

Running an LLM locally is significantly more private than using cloud-based assistants, but there are still best practices to follow.

---

## 🔐 Recommended Hardening Steps

### 1. Restrict Network Access

Ensure OpenWebUI and Ollama are bound to localhost only:

- Do NOT bind to `0.0.0.0` or external IP addresses
- Block external access via Windows Firewall

```powershell
# Block inbound Docker ports as a rule
New-NetFirewallRule -DisplayName "Block OpenWebUI External" -Direction Inbound -LocalPort 3000,11434 -Protocol TCP -Action Block
```

---

### 2. Enable Authentication in OpenWebUI

- Go to `http://localhost:3000/settings`
- Enable user login with a secure password

---

### 3. Log Control & Cleanup

- Disable prompt history in OpenWebUI (Settings > Privacy)
- Clear Docker/OpenWebUI logs regularly
- Avoid syncing `.ollama` and OpenWebUI folders to cloud services

---

### 4. Use a Non-Admin Account

- Create a standard user account to run this project
- Do not use an account with full administrative rights unless required

---

### 5. Resource Awareness

- Heavy models may impact laptop thermals, fan noise, and battery
- Avoid running `ollama` continuously while on battery power

---

## 🔐 RAG Deserialization Security Note

The RAG feature of BYO-SecAI uses LangChain's FAISS vector store. Starting in LangChain v0.2.2, deserializing FAISS indexes requires the following flag:

```python
FAISS.load_local("vector_index", embedding, allow_dangerous_deserialization=True)
```

This flag is **safe to enable only** if:
- You generated the vector index yourself
- You trust the content of your local vector files
- You are not loading `.faiss` or `.pkl` files from an untrusted third party

If you load malicious pickle files from unknown sources, it may lead to arbitrary code execution.

📌 **NEVER** set `allow_dangerous_deserialization=True` on files from the internet unless fully inspected.

---

## ⚠️ Disclaimer

This project is provided **as-is** for personal use in cybersecurity research and educational purposes only.  
We make **no warranties** regarding performance, security, data privacy, or compatibility.

**You are solely responsible** for how you run, extend, or expose this assistant.

- Do not expose the AI API to the internet.
- Do not use it to process sensitive company or customer data without proper controls.
- Do not execute unverified code via this assistant.

By using this project, **you agree that the authors and contributors are not liable for any loss, damage, or misuse** of this tool or any of its components.

---

Stay safe, stay local.
