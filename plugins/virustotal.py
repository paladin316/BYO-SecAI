import os, yaml, requests

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)


# Load config once per invocation
with open(os.path.join(os.getcwd(), "config.yaml")) as f:
    cfg = yaml.safe_load(f)
API_KEY = cfg.get("virustotal_api_key")

def run(ioc: str) -> dict:
    if not API_KEY:
        return {"source":"virustotal","ioc":ioc,"error":"Missing virustotal_api_key in config.yaml"}
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
    headers = {"x-apikey": API_KEY}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 200:
        return {"source":"virustotal","ioc":ioc,"result":resp.json().get("data")}
    return {"source":"virustotal","ioc":ioc,"error":resp.text}
