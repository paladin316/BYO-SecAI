# BYO-SecAI Auto Dependency Installer
import subprocess
import sys

required_packages = [
    "pypdf",
    "requests",
    "faiss-cpu",
    "pandas",
    "tqdm",
    "sentence-transformers",
    "langchain",
    "langchain-community",
    "langchain-huggingface"
]

def install(package):
    try:
        print(f"Installing: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")

if __name__ == "__main__":
    print("🛠️ Installing all required BYO-SecAI RAG dependencies...\n")
    for pkg in required_packages:
        install(pkg)
    print("\n✅ All dependencies installation attempts complete.")