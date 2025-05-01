import os
import yaml

# Load API keys and settings from config.yaml
with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as f:
    cfg = yaml.safe_load(f)

VT_KEY = cfg.get("virustotal_api_key")
AIB_KEY = cfg.get("abuseipdb_api_key")
US_KEY = cfg.get("urlscan_api_key")
YARA_DIR = cfg.get("yara_rules_dir", "yara_rules")