#!/bin/bash

# JobHack Development Startup Script

echo "🚀 Starting JobHack Development Environment..."

# Check if running in project root
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check for .env files
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env not found. Copying from .env.example..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "⚠️  Warning: frontend/.env.local not found. Copying from .env.example..."
    cp frontend/.env.example frontend/.env.local
    echo "📝 Please edit frontend/.env.local with your configuration"
fi

# Start with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d postgres redis

# Wait for services to be healthy
echo "⏳ Waiting for database to be ready..."
sleep 5

# Check if backend dependencies are installed
if [ ! -d "backend/venv" ]; then
    echo "📦 Installing backend dependencies..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend
echo "🔧 Starting backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Start frontend
echo "⚛️  Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ JobHack is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Handle Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; docker-compose down; echo '✅ All services stopped'; exit 0" INT

# Wait for processes
wait
