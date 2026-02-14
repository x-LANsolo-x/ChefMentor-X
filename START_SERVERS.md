# 🚀 Starting ChefMentor X Servers

## Current Status

✅ **Frontend Server:** Running on http://localhost:8081 (Expo Dev Server)
⚠️ **Backend Server:** Not yet running - needs manual start

---

## 📋 Quick Start Instructions

### Step 1: Start Backend Server

**Open a new PowerShell window and run:**

```powershell
cd "C:\Users\kumar\Downloads\hk cooking\hk cooking\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Verify it's working:**
- Open browser: http://localhost:8000/docs
- You should see FastAPI Swagger documentation

---

### Step 2: Frontend is Already Running

✅ The frontend Expo server is running on port 8081

**To access it:**
1. Look for the PowerShell window with "Metro waiting on exp://"
2. Or open: http://localhost:8081
3. Press `w` to open in web browser
4. Press `a` for Android emulator
5. Press `i` for iOS simulator (Mac only)
6. Scan QR code with Expo Go app on your phone

---

## 🔧 Troubleshooting

### Backend Won't Start?

**Check the error in the PowerShell window. Common issues:**

1. **Database Error:**
   ```powershell
   cd backend
   .\venv\Scripts\python.exe -m alembic upgrade head
   ```

2. **Port Already in Use:**
   ```powershell
   # Find process using port 8000
   netstat -ano | findstr :8000
   # Kill it (replace PID with actual number)
   taskkill /PID <PID> /F
   ```

3. **Missing Dependencies:**
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

---

### Frontend Issues?

**If Expo isn't starting:**

```powershell
cd frontend-v1
npm install
npx expo start --clear
```

---

## 📊 Verify Everything is Working

### Backend Health Check:
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
```

Should return: `{"status":"healthy"}`

### Frontend Check:
Open browser: http://localhost:8081

Should see Expo Dev Tools

---

## 🎯 Quick Access URLs

**Once both servers are running:**

- **Backend API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health
- **Frontend (Web):** http://localhost:8081 (press `w`)
- **Frontend (Expo):** http://localhost:8081

---

## 💡 Next Steps After Servers Start

1. **Open Frontend in Browser:**
   - Go to the frontend PowerShell window
   - Press `w` for web

2. **Test the App:**
   - Login with test credentials
   - Browse recipes
   - Try voice commands
   - Test failure analysis

3. **Follow Testing Guide:**
   - Open `README_TESTING.md`
   - Follow the testing checklist
   - Document any issues

---

## 🆘 Still Having Issues?

### Check These:

1. **Python Version:**
   ```powershell
   cd backend
   .\venv\Scripts\python.exe --version
   ```
   Should be Python 3.10+

2. **Node Version:**
   ```powershell
   node --version
   ```
   Should be v16+

3. **Ports in Use:**
   ```powershell
   netstat -ano | findstr ":8000"
   netstat -ano | findstr ":8081"
   ```

### Check Logs:

Look at the PowerShell windows for error messages. Common errors:

- `ModuleNotFoundError` → Run `pip install -r requirements.txt`
- `Database error` → Run `alembic upgrade head`
- `Port in use` → Kill the process using the port
- `Permission denied` → Run PowerShell as Administrator

---

## 📝 Manual Start Commands Summary

**Terminal 1 - Backend:**
```powershell
cd "C:\Users\kumar\Downloads\hk cooking\hk cooking\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd "C:\Users\kumar\Downloads\hk cooking\hk cooking\frontend-v1"
npx expo start
```

---

**Good luck! The frontend is already running on port 8081. Just start the backend and you're ready to test! 🚀**
