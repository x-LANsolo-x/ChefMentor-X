# 🚀 ChefMentor X - Testing Quick Start

## ⚡ 5-Minute Setup

### Option 1: Automated Setup (Recommended)

**Windows:**
```powershell
.\START_TESTING.ps1
```

**Mac/Linux:**
```bash
chmod +x START_TESTING.sh
./START_TESTING.sh
```

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend-v1
npm install
npx expo start
```

---

## 🎯 What to Test (Priority Order)

### 🔴 **CRITICAL - Must Work** (20 min)

1. **Voice Commands** 🎤
   - Start cooking session
   - Say "Next step" → Should advance
   - Say "Repeat" → Should re-read
   - Say "Set timer 2 minutes" → Timer starts

2. **Failure Analysis** 📸
   - Take/upload photo of food
   - Fill context questions
   - Submit for AI analysis
   - Review diagnosis results

3. **Live Cooking** 🍳
   - Browse recipes
   - Start cooking
   - Navigate steps
   - Complete session

### 🟡 **IMPORTANT - Should Work** (15 min)

4. **Authentication**
   - Login/logout
   - Registration

5. **Recipe Features**
   - Search recipes
   - Filter recipes
   - View details

6. **AI Mentor**
   - Ask AI for tips
   - Review suggestions

### 🟢 **NICE TO HAVE** (10 min)

7. **Profile & Settings**
   - View profile
   - Check history
   - Change settings

---

## 📋 Quick Test Checklist

Print this out or keep it handy:

```
□ Backend running (http://localhost:8000/docs)
□ Frontend running (Expo DevTools)
□ Login works
□ Recipe list loads
□ Can start cooking session
□ Voice "Next step" works
□ Voice "Set timer" works
□ Camera/photo upload works
□ AI analysis completes
□ Results show diagnosis
□ No app crashes
```

---

## 🐛 Found a Bug?

### Quick Bug Report:

**What:** <!-- Describe issue -->  
**Where:** <!-- Which screen/feature -->  
**How to reproduce:**
1. 
2. 
3. 

**Screenshot:** <!-- Take a screenshot -->

Save to: `bugs_found.md`

---

## 💡 Testing Tips

✅ **DO:**
- Test on real device if possible
- Take screenshots of everything
- Test voice commands in quiet environment
- Use actual food photos for analysis
- Try edge cases (bad internet, empty forms)

❌ **DON'T:**
- Skip authentication testing
- Ignore error messages
- Test only happy paths
- Rush through tests

---

## 🎬 5-Minute Smoke Test

If you only have 5 minutes:

1. **Launch** → Login (30 sec)
2. **Cook Tab** → Browse recipes (1 min)
3. **Start Cooking** → Test voice "Next step" (2 min)
4. **Analyze Tab** → Upload photo (1 min)
5. **Check** → No crashes? ✅ Basic functionality works!

---

## 📊 After Testing

1. Fill out `TEST_RESULTS_TEMPLATE.md`
2. Create GitHub issues for bugs
3. Share results with team
4. Prioritize fixes

---

## 🆘 Help & Resources

- **Full Testing Guide:** `VISUAL_TESTING_GUIDE.md`
- **API Documentation:** http://localhost:8000/docs
- **Test Results Template:** `TEST_RESULTS_TEMPLATE.md`
- **Setup Issues:** Check `SETUP.md`

---

## 🎯 Success Criteria

**Ready for Production if:**
- ✅ All voice commands work (7/7)
- ✅ AI analysis completes successfully
- ✅ No crashes during 30-min session
- ✅ Core features work on 2+ devices
- ✅ Performance acceptable (< 3s loads)

**Needs Work if:**
- ⚠️ Voice commands < 5/7 working
- ⚠️ Occasional crashes
- ⚠️ Slow performance (> 5s loads)

**Not Ready if:**
- ❌ Cannot login
- ❌ Cannot start cooking
- ❌ Frequent crashes
- ❌ AI analysis fails

---

**Good luck testing! 🎉**

Remember: Finding bugs now is GOOD - it means we can fix them before users find them!
