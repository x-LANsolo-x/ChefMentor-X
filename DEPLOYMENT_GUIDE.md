# 🚀 ChefMentor X - Production Deployment Guide

This guide covers deploying ChefMentor X to production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Monitoring & Observability](#monitoring--observability)

---

## Prerequisites

### Required Services
- **PostgreSQL 15+** - Primary database
- **Redis 7+** - Caching and session storage
- **Cloudinary** - Image storage
- **Google OAuth** - Authentication
- **Gemini API** - AI recipe generation and analysis
- **Groq API** - Voice transcription (Whisper)

### Optional Services
- **RecipeDB API** - External recipe database
- **FlavorDB API** - Flavor pairing recommendations
- **PostHog** - Product analytics
- **Sentry** - Error tracking

---

## Backend Deployment

### Option 1: Docker Deployment (Recommended)

1. **Build and Run with Docker Compose**
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f backend
```

2. **Run Database Migrations**
```bash
docker-compose exec backend alembic upgrade head
```

3. **Seed Initial Data (Optional)**
```bash
docker-compose exec backend python seed_recipes.py
```

### Option 2: Platform as a Service (PaaS)

#### Render.com
1. Create new Web Service
2. Connect your GitHub repository
3. Configure build & start commands:
   - Build: `pip install -r requirements.txt`
   - Start: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.production`
5. Add PostgreSQL and Redis services

#### Railway.app
1. Create new project from GitHub
2. Add PostgreSQL and Redis plugins
3. Set environment variables
4. Deploy automatically on push

#### Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login and launch
fly auth login
fly launch

# Deploy
fly deploy
```

### Option 3: Traditional VPS (DigitalOcean, AWS EC2, etc.)

1. **Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install PostgreSQL & Redis
sudo apt install postgresql redis-server

# Install Nginx
sudo apt install nginx
```

2. **Setup Application**
```bash
# Clone repository
git clone https://github.com/yourusername/chefmentor-x.git
cd chefmentor-x/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env.production
nano .env.production  # Edit with production values
```

3. **Setup Systemd Service**
Create `/etc/systemd/system/chefmentor.service`:
```ini
[Unit]
Description=ChefMentor X API
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/chefmentor-x/backend
Environment="PATH=/var/www/chefmentor-x/backend/venv/bin"
ExecStart=/var/www/chefmentor-x/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable chefmentor
sudo systemctl start chefmentor
sudo systemctl status chefmentor
```

4. **Configure Nginx**
Create `/etc/nginx/sites-available/chefmentor`:
```nginx
server {
    listen 80;
    server_name api.chefmentorx.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/chefmentor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.chefmentorx.com
```

---

## Frontend Deployment

### Option 1: Expo EAS Build (Recommended for Mobile)

1. **Install EAS CLI**
```bash
npm install -g eas-cli
```

2. **Login and Configure**
```bash
cd frontend-v1
eas login
eas build:configure
```

3. **Build for App Stores**
```bash
# iOS
eas build --platform ios --profile production

# Android
eas build --platform android --profile production
```

4. **Submit to Stores**
```bash
# iOS App Store
eas submit --platform ios

# Google Play Store
eas submit --platform android
```

### Option 2: Web Deployment (Vercel/Netlify)

If you have a web version:
```bash
# Build web version
npx expo export:web

# Deploy to Vercel
vercel --prod

# Or deploy to Netlify
netlify deploy --prod --dir=web-build
```

---

## Database Setup

### PostgreSQL Configuration

1. **Create Database**
```sql
CREATE DATABASE chefmentor_prod;
CREATE USER chefmentor WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE chefmentor_prod TO chefmentor;
```

2. **Run Migrations**
```bash
cd backend
alembic upgrade head
```

3. **Backup Strategy**
```bash
# Daily backup cron job
0 2 * * * pg_dump -U chefmentor chefmentor_prod | gzip > /backups/chefmentor_$(date +\%Y\%m\%d).sql.gz
```

### Redis Configuration

Edit `/etc/redis/redis.conf`:
```conf
# Security
requirepass your_redis_password
bind 127.0.0.1

# Performance
maxmemory 256mb
maxmemory-policy allkeys-lru
```

---

## Environment Configuration

### Critical Environment Variables

**Backend (.env.production)**
```bash
# Database - Use managed service or your PostgreSQL instance
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# JWT - Generate secure random key
JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# AI Services
GEMINI_API_KEY=your-key
GROQ_API_KEY=your-key

# File Storage
CLOUDINARY_CLOUD_NAME=your-name
CLOUDINARY_API_KEY=your-key
CLOUDINARY_API_SECRET=your-secret

# Security
CORS_ORIGINS=https://yourdomain.com
DEBUG=False
ENVIRONMENT=production
```

**Frontend (app.json)**
```json
{
  "expo": {
    "extra": {
      "apiUrl": "https://api.chefmentorx.com",
      "environment": "production"
    }
  }
}
```

---

## Monitoring & Observability

### Error Tracking (Sentry)

1. **Install Sentry**
```bash
pip install sentry-sdk[fastapi]
```

2. **Configure in main.py**
```python
import sentry_sdk
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1
)
```

### Analytics (PostHog)

Frontend integration:
```typescript
import PostHog from 'posthog-react-native';

const posthog = new PostHog(
  'your-api-key',
  { host: 'https://app.posthog.com' }
);
```

### Health Checks

Backend health endpoint: `GET /health`
```bash
curl https://api.chefmentorx.com/health
```

### Logging

Use structured logging:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Performance Optimization

### Backend
- Enable gzip compression
- Use Redis caching for frequent queries
- Implement database connection pooling
- Use CDN for static assets

### Frontend
- Optimize images with Cloudinary transformations
- Implement code splitting
- Enable Hermes on React Native
- Use FlatList for long lists

---

## Security Checklist

- [ ] All secrets in environment variables (never in code)
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Rate limiting configured
- [ ] CORS properly configured (no wildcards in production)
- [ ] Database backups automated
- [ ] Error messages don't expose sensitive data
- [ ] JWT secret is strong and rotated periodically
- [ ] Dependencies are up to date (run `npm audit` / `pip check`)
- [ ] API authentication required for sensitive endpoints
- [ ] Input validation on all endpoints

---

## Rollback Procedure

If deployment fails:

1. **Backend Rollback**
```bash
# Docker
docker-compose down
docker-compose up -d --force-recreate

# Systemd
sudo systemctl stop chefmentor
git checkout previous-version
sudo systemctl start chefmentor
```

2. **Database Rollback**
```bash
# Downgrade one migration
alembic downgrade -1

# Restore from backup
psql chefmentor_prod < backup.sql
```

---

## Support & Troubleshooting

### Common Issues

**Database Connection Failed**
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify firewall rules allow connection

**CORS Errors**
- Update CORS_ORIGINS in backend .env
- Ensure frontend API_URL is correct

**Image Upload Failing**
- Verify Cloudinary credentials
- Check file size limits

### Logs

```bash
# Backend logs
docker-compose logs -f backend
# or
sudo journalctl -u chefmentor -f

# Database logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

---

## Maintenance

### Regular Tasks
- Weekly: Review error logs
- Monthly: Update dependencies
- Quarterly: Security audit
- Annually: SSL certificate renewal (auto with Let's Encrypt)

### Database Maintenance
```sql
-- Vacuum and analyze
VACUUM ANALYZE;

-- Check database size
SELECT pg_size_pretty(pg_database_size('chefmentor_prod'));
```

---

## Cost Estimation

### Minimal Production Setup (Estimated)
- **Backend Hosting** (Render/Railway): $7-20/month
- **PostgreSQL** (Managed): $15-25/month
- **Redis** (Managed): $10-15/month
- **Cloudinary** (Free tier): $0
- **Domain & SSL**: $12/year
- **Total**: ~$40-60/month

### Scaling Considerations
- Add load balancer at 1000+ concurrent users
- Separate read replica for database at 10k+ daily users
- CDN for global distribution
