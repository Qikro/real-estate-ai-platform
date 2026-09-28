@echo off
TITLE Real Estate AI Operations Platform - Hyderabad
echo =====================================================================
echo    REAL ESTATE AI OPERATIONS PLATFORM (HYDERABAD & GLOBAL)
echo    Powered by 10 Specialized AI Agents & Central Master Orchestrator
echo =====================================================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [*] Installing required packages...
    venv\Scripts\pip install fastapi uvicorn sqlalchemy pydantic httpx jinja2 python-multipart pyjwt passlib bcrypt reportlab openpyxl pytest pytest-asyncio
)

echo [*] Seeding database and generating initial underwriting models...
venv\Scripts\python seed_data.py

echo [*] Launching Real Estate AI Operations Server on http://localhost:8000 ...
echo [*] Open your browser and navigate to: http://localhost:8000
echo [*] Interactive API Docs (Swagger): http://localhost:8000/docs
echo.
venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
pause
