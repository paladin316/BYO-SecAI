import os, yaml, time, requests

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)


with open(os.path.join(os.getcwd(), "config.yaml")) as f:
    cfg = yaml.safe_load(f)
API_KEY = cfg.get("urlscan_api_key")

def run(ioc: str) -> dict:
    if not API_KEY:
        return {"source":"urlscan","ioc":ioc,"error":"Missing urlscan_api_key in config.yaml"}
    submit_url = "https://urlscan.io/api/v1/scan/"
    headers = {"API-Key": API_KEY, "Content-Type": "application/json"}
    resp = requests.post(submit_url, headers=headers, json={"url": ioc}, timeout=30)
    if resp.status_code != 200:
        return {"source":"urlscan","ioc":ioc,"error":resp.text}
    scan_id = resp.json().get("uuid")
    for _ in range(12):
        time.sleep(5)
        r2 = requests.get(f"https://urlscan.io/api/v1/result/{scan_id}/", timeout=30)
        if r2.status_code == 200:
            return {"source":"urlscan","ioc":ioc,"result":r2.json()}
    return {"source":"urlscan","ioc":ioc,"error":"Scan timed out"}
