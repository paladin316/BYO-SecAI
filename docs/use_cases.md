# 🔍 BYO-SecAI Example Use Cases (CLI Assistant)

The following examples showcase how you can use the `jarvis_no_voice.py` CLI assistant in real-world security operations, threat hunting, and research.

---

## 1. 🎯 MITRE ATT&CK Lookup

```bash
python scripts/jarvis_no_voice.py
```

Prompt:
```
What does MITRE technique T1059 cover?
```

---

## 2. 🕵️ IOC Investigation

```
What does the domain download.evilcorp.biz suggest?
```

---

## 3. 🧠 Threat Actor Summary

```
Summarize APT29 activity from 2023.
```

---

## 4. 🧪 Decode Obfuscated Commands

```
Explain this command: powershell -nop -w hidden -enc UwB...A==
```

---

## 5. 🧬 Generate YARA Rules

```
Write a YARA rule for detecting Cobalt Strike DLLs.
```

---

## 6. 📟 Triage an Alert

```
What should I do if I see WMI spawning cmd.exe in CrowdStrike?
```

---

## 7. 🛡️ Write an IR Playbook

```
Write a short IR playbook for credential dumping.
```

---

## 8. 🔎 Explain Log Field

```
What does event_subtype=CreateRemoteThread mean?
```

---

## 9. 🚨 Detect Data Exfiltration

```
What are common data exfiltration methods over DNS?
```

---

## 10. 🔐 Security Recommendations

```
How should I secure RDP in an enterprise?
```

---

🧠 *These queries run locally through Ollama models (like `phi`, `mistral`, or `llama3`) and never leave your machine.* Perfect for air-gapped security research, threat hunting, and IR.