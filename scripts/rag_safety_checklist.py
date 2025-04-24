# BYO-SecAI RAG Safety Checklist Validator
import os
from pathlib import Path

def check_faiss_index():
    vector_path = Path("vector_index")
    if not vector_path.exists():
        print("❌ vector_index/ directory not found.")
        return False
    files = list(vector_path.glob("*"))
    if not files:
        print("❌ No files found in vector_index/. Did you run --ingest?")
        return False
    print("✅ vector_index/ exists and contains files.")
    return True

def check_log_output():
    log_path = Path("logs")
    if not log_path.exists():
        print("❌ logs/ directory missing.")
        return False
    logs = list(log_path.glob("*.txt"))
    if not logs:
        print("❌ No log files found in logs/.")
        return False
    print(f"✅ Found {len(logs)} log file(s) in logs/.")
    return True

def check_security_flag():
    try:
        with open("scripts/rag_ingest_and_query.py", "r", encoding="utf-8") as f:
            contents = f.read()
        if "allow_dangerous_deserialization=True" in contents:
            print("✅ Deserialization flag correctly included in script.")
            return True
        else:
            print("❌ Deserialization flag missing in rag_ingest_and_query.py.")
            return False
    except FileNotFoundError:
        print("❌ rag_ingest_and_query.py not found.")
        return False

def main():
    print("🛡️ BYO-SecAI RAG Safety Checklist\n")
    results = [
        check_faiss_index(),
        check_log_output(),
        check_security_flag()
    ]
    if all(results):
        print("\n🎉 All safety checks passed.")
    else:
        print("\n⚠️ One or more safety checks failed. Please review.")

if __name__ == "__main__":
    main()