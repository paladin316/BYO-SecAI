# BYO-SecAI Streamlit Config Patch Script
$streamlitConfigPath = "$env:USERPROFILE\.streamlit\config.toml"

if (-Not (Test-Path -Path (Split-Path $streamlitConfigPath))) {
    New-Item -ItemType Directory -Path (Split-Path $streamlitConfigPath) -Force
}

$configContent = @"
[server]
runOnSave = false
fileWatcherType = "none"
"@

$configContent | Set-Content -Path $streamlitConfigPath -Force

Write-Host "✅ Streamlit config patched at $streamlitConfigPath" -ForegroundColor Green
pause