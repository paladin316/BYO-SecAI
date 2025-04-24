
import requests

def ask_jarvis(prompt):
    payload = {
        "model": "phi",
        "messages": [
            {"role": "system", "content": "You are Jarvis, a cybersecurity assistant helping Paladin316."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post("http://localhost:3000/api/v1/chat/completions", json=payload, timeout=30)
        if r.status_code == 200:
            return r.json().get("choices", [{}])[0].get("message", {}).get("content", "No reply.")
        else:
            return f"Jarvis API error: {r.status_code}"
    except Exception as e:
        return f"Error contacting Jarvis: {e}"

if __name__ == "__main__":
    print(ask_jarvis("What is MITRE technique T1059?"))
