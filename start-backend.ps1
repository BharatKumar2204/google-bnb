Write-Host "Starting AI News Verification Backend..." -ForegroundColor Green
Set-Location -Path "$PSScriptRoot\mcp_server"
python run_server.py
