import os, yaml, requests

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)


with open(os.path.join(os.getcwd(), "config.yaml")) as f:
    cfg = yaml.safe_load(f)
API_KEY = cfg.get("abuseipdb_api_key")

def run(ioc: str) -> dict:
    if not API_KEY:
        return {"source":"abuseipdb","ioc":ioc,"error":"Missing abuseipdb_api_key in config.yaml"}
    url = "https://api.abuseipdb.com/api/v2/check"
    params = {"ipAddress": ioc, "maxAgeInDays": 90}
    headers = {"Key": API_KEY, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 200:
        return {"source":"abuseipdb","ioc":ioc,"result":resp.json().get("data")}
    return {"source":"abuseipdb","ioc":ioc,"error":resp.text}
