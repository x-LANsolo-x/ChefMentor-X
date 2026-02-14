@echo off
echo ==========================================
echo ChefMentor X - Robust Launcher
echo ==========================================

echo 1. Stopping existing processes (Ports 8000, 8081)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8081" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo.
echo 2. Launching Backend...
REM Start Backend (auto install pip packages)
start "ChefMentor Backend" cmd /k "cd backend && venv\Scripts\activate && pip install -r requirements.txt && cls && echo [Starting FastAPI Server]... && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo 3. Launching Frontend...
REM Start Frontend (auto install npm packages)
start "ChefMentor Frontend" cmd /k "cd frontend-v1 && npm install && echo [Installed npm dependencies] && cls && echo [Starting Expo Bundler]... && npx expo start --clear"

echo.
echo ==========================================
echo Servers are launching in new windows!
echo - Backend: http://localhost:8000
echo - Frontend: Scan QR code with Expo Go.
echo ==========================================
pause
