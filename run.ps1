# PowerShell Launcher for Real Estate AI Operations Platform
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   REAL ESTATE AI OPERATIONS PLATFORM (HYDERABAD & GLOBAL)" -ForegroundColor Green
Write-Host "   Powered by 10 Specialized AI Agents & Central Master Orchestrator" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "[*] Setting up Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[*] Installing backend dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\pip install fastapi uvicorn sqlalchemy pydantic httpx jinja2 python-multipart pyjwt passlib bcrypt reportlab openpyxl pytest pytest-asyncio
}

Write-Host "[*] Initializing database and running automated test suite..." -ForegroundColor Cyan
.\venv\Scripts\pytest tests/test_suite.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Tests failed. Please check error output." -ForegroundColor Red
    exit 1
}

Write-Host "[*] Database seeded and verified. Starting server on http://localhost:8000 ..." -ForegroundColor Green
Write-Host "    Web Dashboard: http://localhost:8000" -ForegroundColor White
Write-Host "    API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
.\venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
