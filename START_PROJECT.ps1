#!/usr/bin/env pwsh
# ChefMentor X - One-Click Startup Script (Windows/PowerShell)
# This script starts both backend and frontend servers

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🍳 ChefMentor X - Starting Development Servers" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "❌ Error: backend\.env not found!" -ForegroundColor Red
    Write-Host "`nThis is your first time? Run the setup first:" -ForegroundColor Yellow
    Write-Host "  1. cd backend" -ForegroundColor White
    Write-Host "  2. cp .env.example .env" -ForegroundColor White
    Write-Host "  3. Edit .env with your credentials" -ForegroundColor White
    Write-Host "  4. python setup_database.py`n" -ForegroundColor White
    exit 1
}

# Function to start backend
function Start-Backend {
    Write-Host "📡 Starting Backend Server..." -ForegroundColor Green
    Push-Location backend
    
    # Activate virtual environment
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & venv\Scripts\Activate.ps1
    }
    
    # Start backend
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WorkingDirectory $PWD
    
    Pop-Location
    Start-Sleep -Seconds 2
    Write-Host "✅ Backend started at http://localhost:8000" -ForegroundColor Green
}

# Function to start frontend
function Start-Frontend {
    Write-Host "`n📱 Starting Frontend App..." -ForegroundColor Green
    Push-Location frontend-v1
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WorkingDirectory $PWD
    
    Pop-Location
    Start-Sleep -Seconds 2
    Write-Host "✅ Frontend started - scan QR code with Expo Go app" -ForegroundColor Green
}

# Start both servers
Start-Backend
Start-Frontend

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✨ Both servers are starting!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Backend API Docs: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/docs" -ForegroundColor Blue

Write-Host "`nTo stop servers: Close the PowerShell windows or press Ctrl+C`n" -ForegroundColor Yellow
