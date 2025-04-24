import requests

def ask_jarvis(prompt):
    payload = {
        "model": "phi",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["message"]["content"]
        else:
            return f"Jarvis API error: {r.status_code}"
    except Exception as e:
        return f"Error contacting Jarvis: {e}"

if __name__ == "__main__":
    print(ask_jarvis("What is MITRE technique T1059?"))