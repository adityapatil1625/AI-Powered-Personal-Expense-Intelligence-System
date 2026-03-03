@echo off
REM Production Deployment Script for Windows
REM This script sets up and deploys the Expense Intelligence application

echo 🚀 Starting Expense Intelligence Deployment (Windows)...

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy backend\.env.example .env
    echo ✅ .env created. Please update it with your configuration.
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements.txt
pip install gunicorn

REM Initialize database
echo 🗄️  Initializing database...
python -c "from app.database.db import init_db; init_db(); print('✅ Database initialized')"

REM Start application
echo ✅ Deployment complete!
echo 🚀 Starting production server...
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app.main:app

pause
