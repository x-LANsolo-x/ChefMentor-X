# 👥 ChefMentor X - Team Member Setup Guide

**Quick setup instructions for new developers**

---

## 🚀 Quick Start (5 minutes)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/x-LANsolo-x/BugOff.git
cd BugOff
```

### **Step 2: Backend Setup**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 3: Configure Database**

Create `.env` file in `backend/` directory:

```bash
# Windows:
New-Item .env -ItemType File

# Mac/Linux:
touch .env
```

Add this **ONE LINE** to your `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway
```

### **Step 4: Add API Keys (Optional)**

Add these lines to your `.env` file if you want to test AI features:

```env
# AI Keys (get from team lead or create your own)
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=dev-secret-key-change-in-production-12345678
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=*
ENVIRONMENT=development
DEBUG=true
```

### **Step 5: Run Backend**

```bash
# Make sure you're in backend/ directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test it:** Open http://localhost:8000/docs

---

## 📱 Frontend Setup

### **Step 1: Install Node.js**
- Download from: https://nodejs.org/
- Recommended: LTS version (v18+)

### **Step 2: Frontend Dependencies**

```bash
# Navigate to frontend
cd frontend-v1

# Install dependencies
npm install

# Start Expo server
npx expo start
```

### **Step 3: Run on Device/Emulator**

**Options:**
- Press `w` - Open in web browser
- Press `a` - Open in Android emulator
- Press `i` - Open in iOS simulator (Mac only)
- Scan QR code with Expo Go app on your phone

---

## 🗄️ Database Access

### **Using pgAdmin / DBeaver / DataGrip:**

1. Open your database tool
2. Create new connection
3. Enter these details:

```
Host: yamanote.proxy.rlwy.net
Port: 18960
Database: railway
Username: postgres
Password: PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD
SSL: Required
```

### **Using Command Line (psql):**

```bash
psql "postgresql://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway?sslmode=require"
```

---

## 📚 Project Structure

```
BugOff/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # App entry point
│   ├── tests/              # Backend tests
│   ├── .env               # Your environment variables
│   └── requirements.txt    # Python dependencies
│
├── frontend-v1/            # React Native frontend
│   ├── src/
│   │   ├── screens/       # App screens
│   │   ├── components/    # Reusable components
│   │   ├── stores/        # MobX state management
│   │   └── services/      # API clients
│   └── package.json       # Node dependencies
│
└── docs/                  # Documentation
```

---

## 🧪 Testing Your Setup

### **Backend Test:**

```bash
# In backend/ directory
curl http://localhost:8000/health

# Expected response:
{"status": "healthy"}
```

### **Database Test:**

```bash
# In backend/ directory with venv activated
python -c "import asyncpg; print('PostgreSQL driver installed ✓')"
```

### **Frontend Test:**

```bash
# In frontend-v1/ directory
npm start

# Should see Expo DevTools in browser
```

---

## 🔑 Getting API Keys

### **Gemini API (Required for AI features)**
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy and add to `.env`

### **Groq API (Required for voice features)**
1. Go to: https://console.groq.com/keys
2. Create new API key
3. Copy and add to `.env`

---

## 💡 Common Issues & Solutions

### **Issue: "Module not found" errors**
```bash
# Backend:
pip install -r requirements.txt

# Frontend:
npm install
```

### **Issue: Database connection fails**
- Check internet connection
- Verify password has no extra spaces
- Ensure Railway service is running
- First connection may take 30-60 seconds

### **Issue: Port 8000 already in use**
```bash
# Windows - find and kill process:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### **Issue: Expo not starting**
```bash
# Clear cache and restart:
npx expo start -c
```

---

## 📖 Useful Commands

### **Backend:**
```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### **Frontend:**
```bash
# Start dev server
npm start

# Clear cache
npx expo start -c

# Run on specific platform
npm run android
npm run ios
npm run web
```

---

## 📞 Getting Help

**Documentation:**
- Full API docs: http://localhost:8000/docs
- README: See main README.md
- Testing guide: See TESTING_COMPLETE_GUIDE.md

**Team Contacts:**
- Project Lead: Kumar Utkarsh
- Email: kumarutkarsh688@gmail.com
- GitHub: https://github.com/x-LANsolo-x/BugOff

**External Resources:**
- FastAPI: https://fastapi.tiangolo.com/
- React Native: https://reactnative.dev/
- Expo: https://docs.expo.dev/
- Railway: https://docs.railway.app/

---

## ✅ Setup Checklist

Before you start coding:

- [ ] Repository cloned
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] `.env` file created with DATABASE_URL
- [ ] Backend starts successfully
- [ ] Can access http://localhost:8000/docs
- [ ] Frontend dependencies installed
- [ ] Expo server starts successfully
- [ ] Can view app in browser/emulator
- [ ] Database connection works
- [ ] API keys added (if needed)

---

**You're ready to start developing! 🎉**

Happy coding! If you encounter any issues, check the troubleshooting section or reach out to the team.
