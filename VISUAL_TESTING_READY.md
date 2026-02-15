# 🎉 Visual Testing Environment Ready!

## ✅ Servers Started Successfully

### **Backend Server**
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Status:** Running ✅

### **Frontend Server** 
- **URL:** http://localhost:8081
- **Expo DevTools:** Open in browser
- **Mobile App:** Scan QR code or press 'w' for web
- **Status:** Running ✅

---

## 📱 How to Start Visual Testing

### **Option 1: Web Browser (Fastest)**
1. Look at the Expo window in PowerShell
2. Press `w` to open in web browser
3. The app will open at http://localhost:8081

### **Option 2: Mobile Device**
1. Install **Expo Go** app on your phone
2. Scan the QR code from the Expo window
3. App will load on your device

### **Option 3: iOS Simulator** (Mac only)
1. Press `i` in the Expo window
2. iOS Simulator will launch

### **Option 4: Android Emulator**
1. Start Android Emulator first
2. Press `a` in the Expo window
3. App will install and run

---

## 🧪 Visual Testing Checklist

Follow this systematic approach:

### **1. Auth & Onboarding (5 min)**
- [ ] Open app - see splash screen
- [ ] Onboarding screens swipe through
- [ ] Login screen - enter credentials
- [ ] Demo mode works

### **2. Recipe List Screen (5 min)**
- [ ] See recipe cards
- [ ] Search functionality
- [ ] Filter by difficulty/time
- [ ] Tap recipe to see details

### **3. Recipe Details Screen (5 min)**
- [ ] Image displays
- [ ] Ingredients list
- [ ] Instructions visible
- [ ] "Start Cooking" button works

### **4. Live Cooking Screen (10 min)**
- [ ] Step-by-step instructions
- [ ] Progress bar updates
- [ ] Timer functionality
- [ ] Pause/Resume works
- [ ] **📸 Camera button** - tap to test live camera
- [ ] **💡 Ask AI button** - get AI tips
- [ ] **🎙️ Voice button** - voice commands
- [ ] Next/Previous steps
- [ ] Complete session

### **5. Live Camera Feature (5 min)** ⭐ NEW
- [ ] Camera opens from cooking screen
- [ ] Live preview visible
- [ ] Flash toggle works
- [ ] Flip camera works
- [ ] Capture photo
- [ ] AI analysis shows
- [ ] Close button returns to cooking

### **6. Analyze Tab (10 min)** ⭐ FULLY FUNCTIONAL
- [ ] Tap Analyze tab
- [ ] **Take Photo** - camera opens
- [ ] **Choose from Gallery** - image picker
- [ ] Image preview shows
- [ ] Remove image works
- [ ] Tap "Analyze This Dish"
- [ ] Context questions appear
- [ ] Select heat/timing/modifications
- [ ] Add notes
- [ ] Submit analysis
- [ ] Loading animation
- [ ] Results screen with diagnosis

### **7. Profile Tab (5 min)** ⭐ EDIT WORKS
- [ ] Profile info displays
- [ ] **Tap "Edit"** in Cooking Profile
- [ ] Modal slides up
- [ ] Edit name
- [ ] Change difficulty level
- [ ] Select dietary preference
- [ ] Save changes
- [ ] Modal closes
- [ ] Changes visible immediately

### **8. Settings (5 min)** ⭐ FULLY FUNCTIONAL
- [ ] Tap Settings icon
- [ ] Toggle voice speed (Slow/Normal/Fast)
- [ ] Toggle beginner mode
- [ ] Toggle wake word
- [ ] Toggle notifications
- [ ] All switches respond
- [ ] Privacy menu works
- [ ] Help & Support works
- [ ] Logout works

---

## 🐛 What to Look For

### **UI Issues:**
- [ ] Text overlapping buttons
- [ ] Buttons covering other elements
- [ ] Images not loading
- [ ] Misaligned elements
- [ ] Spacing problems

### **Functionality:**
- [ ] Buttons don't respond
- [ ] Navigation broken
- [ ] Features not working
- [ ] Errors in console

### **Performance:**
- [ ] Slow loading
- [ ] Laggy animations
- [ ] Stuttering scrolling
- [ ] Memory issues

---

## 📊 Testing Priority

### **Must Test (Critical):**
1. ✅ **Live Camera** - Brand new feature
2. ✅ **Analyze Tab** - Just implemented
3. ✅ **Ask AI** - Just implemented
4. ✅ **Profile Edit** - Just implemented
5. ✅ **Settings** - Just implemented

### **Should Test (Important):**
6. Live Cooking flow
7. Voice commands
8. Recipe browsing

### **Nice to Test:**
9. Onboarding
10. Login flow

---

## 🔧 Troubleshooting

### **Backend Not Responding:**
```powershell
# Check if running
netstat -ano | findstr :8000

# Restart if needed
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

### **Frontend Not Loading:**
```powershell
# Check if running
netstat -ano | findstr :8081

# Restart if needed
cd frontend-v1
npx expo start
```

### **App Crashes:**
- Check PowerShell windows for error messages
- Look at browser console (F12)
- Check backend logs

---

## 📝 Report Issues

For each bug found, note:
1. **Screen/Feature:** Where it happened
2. **Steps to Reproduce:** What you did
3. **Expected:** What should happen
4. **Actual:** What actually happened
5. **Screenshot:** If possible

---

## 🎯 Success Criteria

### **All Features Working:**
- ✅ Camera opens and captures
- ✅ Analyze tab uploads and analyzes
- ✅ Ask AI fetches tips
- ✅ Profile edit saves changes
- ✅ Settings persist
- ✅ No UI overlapping
- ✅ Smooth navigation
- ✅ No crashes

---

**Ready to start testing! 🚀**

Look for the two PowerShell windows:
1. **Backend** - Shows API logs
2. **Frontend** - Shows Expo server with QR code

**Press 'w' in the Expo window to start testing in your browser!**
