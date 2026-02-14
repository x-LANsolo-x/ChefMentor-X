#!/bin/bash
# ChefMentor X - One-Click Startup Script (Mac/Linux)
# This script starts both backend and frontend servers

echo -e "\n========================================"
echo -e "🍳 ChefMentor X - Starting Development Servers"
echo -e "========================================\n"

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "❌ Error: backend/.env not found!\n"
    echo -e "This is your first time? Run the setup first:"
    echo -e "  1. cd backend"
    echo -e "  2. cp .env.example .env"
    echo -e "  3. Edit .env with your credentials"
    echo -e "  4. python setup_database.py\n"
    exit 1
fi

# Start backend in new terminal
echo "📡 Starting Backend Server..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)/backend'\" && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"'
else
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; exec bash" &
    else
        echo "⚠️  No terminal emulator found. Start backend manually:"
        echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    fi
fi

sleep 2
echo "✅ Backend started at http://localhost:8000"

# Start frontend in new terminal
echo -e "\n📱 Starting Frontend App..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)/frontend-v1'\" && npm start"'
else
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd frontend-v1 && npm start; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd frontend-v1 && npm start; exec bash" &
    else
        echo "⚠️  No terminal emulator found. Start frontend manually:"
        echo "   cd frontend-v1 && npm start"
    fi
fi

sleep 2
echo "✅ Frontend started - scan QR code with Expo Go app"

echo -e "\n========================================"
echo -e "✨ Both servers are starting!"
echo -e "========================================\n"

echo -e "Backend API Docs: http://localhost:8000/docs\n"
echo -e "To stop servers: Close the terminal windows or press Ctrl+C\n"
