# 🗄️ ChefMentor X - PostgreSQL Database Credentials

**⚠️ CONFIDENTIAL - DO NOT COMMIT TO PUBLIC REPOSITORIES**

---

## 🔐 Database Access Credentials

### **Production Database (Railway)**

**Provider:** Railway.app  
**Database Type:** PostgreSQL  
**Status:** ✅ Active & Operational

---

## 📋 Connection Details

### **Primary Connection String (For Backend)**
```
postgresql+asyncpg://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway
```

### **Individual Credentials**
| Field | Value |
|-------|-------|
| **Username** | `postgres` |
| **Password** | `PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD` |
| **Host** | `yamanote.proxy.rlwy.net` |
| **Port** | `18960` |
| **Database Name** | `railway` |
| **SSL Mode** | Required (enabled by default) |

---

## 🛠️ Setup Instructions for Team Members

### **Option 1: Using Environment Variables (Recommended)**

1. Create a `.env` file in the `backend/` directory:
   ```bash
   cd backend
   touch .env
   ```

2. Add this line to your `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway
   ```

3. The backend will automatically use this connection string

---

### **Option 2: Direct Connection (For Database Tools)**

Use these credentials in your preferred database client:

**DBeaver / DataGrip / pgAdmin:**
- **Host:** `yamanote.proxy.rlwy.net`
- **Port:** `18960`
- **Database:** `railway`
- **Username:** `postgres`
- **Password:** `PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD`
- **SSL:** Enabled

**Connection URL (standard PostgreSQL):**
```
postgresql://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway
```

---

## 💻 Code Examples

### **Python (asyncpg)**
```python
import asyncpg

async def connect():
    conn = await asyncpg.connect(
        user='postgres',
        password='PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD',
        database='railway',
        host='yamanote.proxy.rlwy.net',
        port=18960
    )
    return conn
```

### **Python (SQLAlchemy)**
```python
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway"

engine = create_async_engine(DATABASE_URL, echo=True)
```

### **Node.js (pg)**
```javascript
const { Client } = require('pg');

const client = new Client({
  user: 'postgres',
  password: 'PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD',
  host: 'yamanote.proxy.rlwy.net',
  port: 18960,
  database: 'railway',
  ssl: { rejectUnauthorized: false }
});

await client.connect();
```

### **.NET (Npgsql)**
```csharp
var connString = "Host=yamanote.proxy.rlwy.net;Port=18960;Username=postgres;Password=PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD;Database=railway;SSL Mode=Require";

await using var conn = new NpgsqlConnection(connString);
await conn.OpenAsync();
```

---

## 📊 Current Database Status

### **Tables (8 total)**
- `users` - 2 user accounts
- `user_profiles` - User cooking profiles
- `recipes` - 5 recipes with details
- `recipe_steps` - 30 instruction steps
- `cooking_sessions` - Live cooking sessions
- `failure_analyses` - Dish failure analysis
- `demo_sessions` - Demo mode data
- `alembic_version` - Database migrations

### **Existing Users**
1. testuser@gmail.com - Test User
2. kumarutkarsh688@gmail.com - Kumar Utkarsh

---

## 🌐 Railway Dashboard Access

**To manage the database (add team members, view metrics, etc.):**

1. **Login to Railway:** https://railway.app/
2. **Account Email:** (You'll need to share Railway account access)
3. **Project:** ChefMentor X
4. **Service:** PostgreSQL

**Railway Dashboard Features:**
- View connection metrics
- Check database size/usage
- Manage backups
- View logs
- Add team members
- Monitor performance

---

## 🔒 Security Best Practices

### **For Team Members:**

1. **Never commit credentials to git**
   - `.env` files are in `.gitignore`
   - Always use environment variables
   - Don't hardcode passwords in code

2. **Keep credentials secure**
   - Don't share in public channels
   - Use secure password managers
   - Don't post in public GitHub issues

3. **Local development**
   - Each developer uses the same production DB OR
   - Set up local PostgreSQL for development
   - Use different `.env` files for dev/prod

4. **Database permissions**
   - Current user has full admin access
   - Be careful with DROP/TRUNCATE commands
   - Test destructive operations locally first

---

## 🛡️ Connection Security

**The connection is secure:**
- ✅ SSL/TLS encrypted
- ✅ Hosted on Railway's secure infrastructure
- ✅ Password is strong (32 characters)
- ✅ Non-standard port (18960) for extra security
- ✅ Limited to authenticated connections only

---

## 📝 Quick Start Checklist

For new team members:

- [ ] Clone the repository
- [ ] Navigate to `backend/` directory
- [ ] Create `.env` file
- [ ] Copy the DATABASE_URL line (see above)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test connection: `python -c "import asyncpg; print('OK')"`
- [ ] Run backend: `uvicorn app.main:app --reload`
- [ ] Verify connection in startup logs

---

## 🆘 Troubleshooting

### **Connection Refused**
- Check internet connection
- Verify firewall allows outbound port 18960
- Ensure Railway service is running

### **Authentication Failed**
- Double-check password (no extra spaces)
- Verify username is exactly `postgres`
- Check if credentials were rotated

### **SSL Error**
- Ensure SSL is enabled in your client
- Use `ssl=True` or `sslmode=require`
- Some clients need `ssl={"sslmode": "require"}`

### **Timeout**
- Railway service might be sleeping (free tier)
- First connection may take 30-60 seconds
- Subsequent connections are faster

---

## 📞 Support Contacts

**Database Issues:**
- Railway Support: https://railway.app/help
- Railway Discord: https://discord.gg/railway

**Project Lead:**
- Kumar Utkarsh (kumarutkarsh688@gmail.com)

---

## 🔄 Rotating Credentials

**If you need to change the password:**

1. Go to Railway dashboard
2. Select PostgreSQL service
3. Variables tab
4. Click "New Variable" or regenerate
5. Update all team members' `.env` files
6. Restart all services

---

## ⚠️ IMPORTANT REMINDERS

1. **DO NOT** commit this file to public repositories
2. **DO NOT** share credentials in public channels
3. **DO** use environment variables
4. **DO** keep backups of important data
5. **DO** notify team if credentials change

---

**Last Updated:** 2026-02-15  
**Database Version:** PostgreSQL (Railway managed)  
**Status:** ✅ Active and Operational
