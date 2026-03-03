#!/bin/bash

# Production Deployment Script
# This script sets up and deploys the Expense Intelligence application

set -e

echo "🚀 Starting Expense Intelligence Deployment..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp backend/.env.example .env
    echo "✅ .env created. Please update it with your configuration."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
pip install gunicorn

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app.database.db import init_db; init_db(); print('✅ Database initialized')"

# Start application
echo "✅ Deployment complete!"
echo "🚀 Starting production server..."
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app.main:app
