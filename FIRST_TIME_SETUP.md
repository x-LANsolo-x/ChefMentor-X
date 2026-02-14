# 🚀 ChefMentor X - First Time Setup (5 Minutes)

This guide will get you from **git clone** to **running app** in 5 minutes.

---

## Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.10+** ([Download](https://www.python.org/downloads/))
- ✅ **Node.js 18+** ([Download](https://nodejs.org/))
- ✅ **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))
- ✅ **Git** ([Download](https://git-scm.com/downloads))

**Optional but recommended:**
- Redis (for caching) - can skip for development
- Expo Go app on your phone (for testing mobile app)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/x-LANsolo-x/BugOff.git
cd BugOff
```

---

## Step 2: Backend Setup (2 minutes)

### 2.1 Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

**Edit `backend/.env` with your text editor:**

The **minimum required** changes:

```env
# 1. Database - Update the password to match your PostgreSQL password
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD_HERE@localhost:5432/chefmentor_dev

# 2. JWT Secret - Generate a new one
# Run: python -c "import secrets; print(secrets.token_hex(32))"
# Then paste the output here:
JWT_SECRET=paste-generated-secret-here

# 3. AI API Keys (Get free keys from these links)
# Gemini: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your-gemini-key-here

# Groq: https://console.groq.com/keys
GROQ_API_KEY=your-groq-key-here

# 4. Cloudinary (for image uploads)
# Sign up: https://cloudinary.com/users/register/free
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Optional:** Google OAuth, Redis, etc. (can skip for now)

### 2.3 Setup Database (Automated!)

```bash
# This script will:
# - Test PostgreSQL connection
# - Create the database
# - Run migrations
# - Seed sample data

python setup_database.py
```

**If you get an error:**

<details>
<summary>❌ "Cannot connect to PostgreSQL"</summary>

**Solution:**
1. Make sure PostgreSQL is running:
   - Windows: Check Services → PostgreSQL should be running
   - Mac: `brew services start postgresql`
   - Linux: `sudo systemctl start postgresql`

2. Check your password in `.env` matches your PostgreSQL password

3. Test manually:
   ```bash
   psql -U postgres
   # Enter your password when prompted
   ```
</details>

<details>
<summary>❌ "psycopg2 module not found"</summary>

**Solution:**
```bash
pip install psycopg2-binary
```
</details>

### 2.4 Start the Backend

```bash
uvicorn app.main:app --reload
```

✅ **Backend is running!** Visit http://localhost:8000/docs to see the API documentation.

---

## Step 3: Frontend Setup (2 minutes)

Open a **new terminal** (keep backend running):

```bash
cd frontend-v1

# Install dependencies
npm install

# Start the app
npm start
```

**You should see:**
```
› Metro waiting on exp://192.168.x.x:8081
› Scan the QR code above with your phone to open the app
```

### 3.1 Test on Your Phone

1. Install **Expo Go** app:
   - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)
   - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. Scan the QR code with:
   - **iPhone:** Camera app
   - **Android:** Expo Go app

3. App should load on your phone! 🎉

### 3.2 Test on Emulator/Simulator

```bash
# iOS (Mac only)
npm run ios

# Android (any OS)
npm run android

# Web browser
npm run web
```

---

## Step 4: Verify Everything Works

### Backend Health Check
Open http://localhost:8000/health - should show:
```json
{
  "status": "healthy",
  "timestamp": "2024-..."
}
```

### Test API Endpoints
Open http://localhost:8000/docs and try:
- `GET /api/v1/recipes` - Should return recipes
- `POST /api/v1/auth/demo-login` - Should get demo token

### Frontend Connection Test
1. Open app on phone/emulator
2. You should see the onboarding screen
3. Tap "Start Cooking" → Should show recipe list

---

## 🎉 You're Done!

Your ChefMentor X setup is complete!

### Quick Start Commands (for next time)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend-v1
npm start
```

---

## Troubleshooting

### Port Already in Use

**Backend (8000):**
```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill
```

**Frontend (8081):**
```bash
# Kill Metro bundler
# Windows:
taskkill /F /IM node.exe

# Mac/Linux:
killall node
```

### Database Connection Issues

**Check PostgreSQL is running:**
```bash
# Windows: Check Services app
# Mac: brew services list
# Linux: sudo systemctl status postgresql
```

**Test connection manually:**
```bash
psql -U postgres -h localhost
# Enter password
# Should connect without errors
```

**Reset database (if corrupted):**
```bash
# Connect to postgres
psql -U postgres

# Drop and recreate
DROP DATABASE IF EXISTS chefmentor_dev;
CREATE DATABASE chefmentor_dev;
\q

# Re-run setup
python setup_database.py
```

### Frontend Won't Connect to Backend

**Update frontend API URL:**
Edit `frontend-v1/src/config/env.ts`:
```typescript
export const API_URL = 'http://YOUR_COMPUTER_IP:8000';
// Replace YOUR_COMPUTER_IP with your actual IP
// Windows: ipconfig
// Mac/Linux: ifconfig
```

---

## Next Steps

- 📖 Read [API_GUIDE.md](API_GUIDE.md) to understand the API
- 🎨 Check [frontend-v1/PHASE_7.2_USAGE_GUIDE.md](frontend-v1/PHASE_7.2_USAGE_GUIDE.md) for app features
- 🚀 Deploy to production: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## Getting Help

- 📋 [Open an issue](https://github.com/x-LANsolo-x/BugOff/issues)
- 📧 Email: shashwatvatsyayan@gmail.com
- 📚 Check existing documentation in the repo

---

**Happy Cooking! 🍳**
