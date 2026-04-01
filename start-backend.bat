@echo off
REM Simple backend startup script
cd /d "%~dp0backend"
call .venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
