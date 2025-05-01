import os, yaml, yara

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

with open(os.path.join(os.getcwd(), "config.yaml")) as f:
    cfg = yaml.safe_load(f)
YARA_DIR = cfg.get("yara_rules_dir", "yara_rules")

def run(ioc: str) -> dict:
    # YARA only makes sense against a file path
    if not os.path.isfile(ioc):
        return {"source":"yara_scanner","ioc":ioc,"error":"IOC is not a file path"}
    rule_files = {
        os.path.splitext(fn)[0]: os.path.join(YARA_DIR, fn)
        for fn in os.listdir(YARA_DIR)
        if fn.lower().endswith((".yar", ".yara"))
    }
    if not rule_files:
        return {"source":"yara_scanner","ioc":ioc,"error":"No rules found in yara_rules_dir"}
    try:
        rules = yara.compile(filepaths=rule_files)
        matches = rules.match(ioc)
        return {"source":"yara_scanner","ioc":ioc,"result":[m.rule for m in matches]}
    except Exception as e:
        return {"source":"yara_scanner","ioc":ioc,"error":str(e)}
