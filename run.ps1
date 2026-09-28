# Gemini AI Hub PowerShell Runner
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "     Starting Gemini AI Hub (FastAPI + Jinja2)" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan

$pythonExe = "python"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\Users\AIDS\anaconda3\python.exe") {
        $pythonExe = "C:\Users\AIDS\anaconda3\python.exe"
    } else {
        Write-Error "Python was not found. Please install Python 3.10+ or check PATH."
        exit 1
    }
}

& $pythonExe run.py
