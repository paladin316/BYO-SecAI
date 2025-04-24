
# BYO-SecAI Setup Script (Optional PowerShell Installer)
# Author: Paladin316 + Aegis (ChatGPT)

Write-Host '`n[INFO] Starting BYO-SecAI Setup...' -ForegroundColor Cyan

# Step 1: Check Python version
Write-Host '`n[STEP] Checking Python version...'
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host '[ERROR] Python not found. Please install Python 3.10 from:' -ForegroundColor Red
    Write-Host '        https://www.python.org/downloads/release/python-31013/'
    exit 1
}

$version = python --version
if ($version -notmatch '3.10') {
    Write-Host "[ERROR] Python 3.10 is required. Detected version: $version" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python 3.10 detected: $version" -ForegroundColor Green

# Step 2: Setup virtual environment
Write-Host '`n[STEP] Setting up Python virtual environment...'
python -m venv jarvis_env
if (-not (Test-Path ".\jarvis_env\Scripts\activate")) {
    Write-Host '[ERROR] Failed to create virtual environment.' -ForegroundColor Red
    exit 1
}
. .\jarvis_env\Scripts\activate

# Step 3: Install Python requirements
Write-Host '`n[STEP] Installing Python modules...'
pip install -r requirements.txt

# Step 4: Start Ollama models
Write-Host '`n[STEP] Starting LLM models with Ollama...'
Start-Process -NoNewWindow -FilePath "ollama" -ArgumentList "run phi"
Start-Process -NoNewWindow -FilePath "ollama" -ArgumentList "run mistral"
Start-Process -NoNewWindow -FilePath "ollama" -ArgumentList "run llama3"

# Step 5: Check Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host '[ERROR] Docker is not running. Please start Docker Desktop manually.' -ForegroundColor Red
    exit 1
}

# Step 6: Start OpenWebUI with Docker
Write-Host '`n[STEP] Starting OpenWebUI...'
cd "$env:USERPROFILE\open-webui"
docker-compose up -d

Write-Host '[✔] Setup complete. Access your assistant at: http://localhost:3000' -ForegroundColor Green
Write-Host 'To test your assistant, run: python .\scripts\jarvis_no_voice.py' -ForegroundColor Cyan
