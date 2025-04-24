
# Recommended Local LLMs – BYO-SecAI

Your BYO-SecAI assistant supports a range of local models via [Ollama](https://ollama.com). This guide explains which models to use for different cybersecurity tasks, as well as hardware considerations.

---

## 🧠 Model Comparison

| Model             | Size   | Best Use Cases                                            | Notes                          |
|------------------|--------|------------------------------------------------------------|--------------------------------|
| **phi**          | 1.7B   | Fast Q&A, ATT&CK mapping, MITRE technique lookup          | Lightweight, fast on CPU       |
| **mistral**      | 7B     | Threat hunt generation, detection design, IR logic        | Best overall for reasoning     |
| **llama2**       | 7B/13B | Report writing, deeper decision-making, planning          | Balanced speed and accuracy    |
| **codellama**    | 7B     | Writing detections (YARA, Sigma), scripting, Python logic | Best for detection engineers   |
| **deepseek-coder** | 6.7B | Large codebase support, multilang detection scripting     | Advanced code assistant        |
| **gemma**        | 2B/7B  | Instruction following, fast secure query assistant        | Great on lower memory systems  |
| **orca-mini**    | 3B     | Efficient logic and response summaries                    | Reliable fallback              |
| **tinyllama**    | 1.1B   | Extremely lightweight models                              | Use on low-end machines        |

---

## 🔄 Model Strategy

| Use Case                      | Primary Model   | Alternate Models       |
|------------------------------|-----------------|------------------------|
| Threat Hunting Q&A           | `mistral`       | `phi`, `gemma`         |
| Detection Logic Brainstorming| `codellama`     | `mistral`, `deepseek`  |
| MITRE/ATT&CK Mapping         | `phi`           | `gemma`, `orca-mini`   |
| Code Generation (YARA, etc)  | `codellama`     | `deepseek-coder`       |
| IR SOP & Playbooks           | `llama2`        | `mistral`              |

---

## 🧪 Example Hardware (Tested by Paladin316)

| Component     | Specs                                   |
|---------------|------------------------------------------|
| CPU           | Intel Core i9-12950HX (12th Gen, 2.3GHz) |
| RAM           | 32 GB DDR4                               |
| Storage       | 954 GB SSD                               |
| GPU           | **NVIDIA RTX A4500 (20GB VRAM)**         |
| OS            | Windows 11 Pro, 64-bit                   |

### 🧠 Why RTX A4500 Works Well

- Easily runs 7B–13B models like `mistral` or `llama2`
- CUDA acceleration for fast inference
- Sufficient VRAM for multitasking LLM + Docker + assistant

---

## 🤖 Assistant Codename

All documentation and tuning were done with support from **Aegis** (My AI Assistant).

