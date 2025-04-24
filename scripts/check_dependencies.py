from langchain_huggingface import HuggingFaceEmbeddings
# BYO-SecAI Dependency Checker
import importlib

required_modules = [
    "pypdf",
    "requests",
    "streamlit",
    "faiss",
    "pandas",
    "tqdm",
    "sentence_transformers",
    "langchain",
    "langchain_community",
    "langchain_huggingface"
]

print("🔍 Checking Python modules for BYO-SecAI RAG...\n")

for module in required_modules:
    try:
        importlib.import_module(module)
        print(f"✅ {module} installed")
    except ImportError:
        print(f"❌ {module} is MISSING. Install with: pip install {module.replace('_', '-')}")