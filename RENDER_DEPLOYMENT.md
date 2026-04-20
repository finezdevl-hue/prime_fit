# PRIME FIT Django - Render Deployment Guide

## Free Plan Deployment on Render

This guide shows how to deploy PRIME FIT Django app on Render's free tier.

### Prerequisites
- Render account (https://render.com)
- GitHub repository with your code
- Environment variables configured

### Deployment Steps

#### 1. Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for Render deployment"
git push
```

#### 2. Create Render Web Service
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `primefit-django`
   - **Environment**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn primefit.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free

#### 3. Add Environment Variables
In Render dashboard, go to Environment:

```
DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=sqlite:///db.sqlite3
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com

# Admin credentials (auto-created during build)
ADMIN_USER=admin
ADMIN_EMAIL=admin@primefit.com
ADMIN_PASSWORD=your-secure-admin-password
```

> **Note**: Generate a secure SECRET_KEY:
> ```python
> from django.core.management.utils import get_random_secret_key
> print(get_random_secret_key())
> ```

#### 4. Create Database (Optional - PostgreSQL)
For production, use PostgreSQL instead of SQLite:

1. Click "New +" → "PostgreSQL"
2. Select Free plan
3. Link to your web service
4. Update `DATABASE_URL` environment variable (auto-populated)

#### 5. Deploy
Push to GitHub - Render will automatically:
- Install dependencies
- Run `build.sh` (collects static files, runs migrations, creates superuser)
- Start the web service

**Admin Login:**
- URL: `https://your-app-name.onrender.com/admin/`
- Username: Value of `ADMIN_USER` env var (default: `admin`)
- Password: Value of `ADMIN_PASSWORD` env var

### Media Files (Important!)
**Render free tier has ephemeral storage** - files deleted on redeploy.

For production, use an external service:
- **AWS S3** (with boto3)
- **Cloudinary** (image hosting)
- **Azure Blob Storage**

Currently, media files are served locally and will be lost on redeployment.

### Static Files
- Handled by **WhiteNoise** middleware
- Automatically collected during build
- No CDN required for free tier

### Troubleshooting

**502 Bad Gateway**
- Check logs: Render dashboard → Logs
- Verify `SECRET_KEY` and `DEBUG` settings
- Run `python manage.py check --deploy`

**CSRF Token Errors**
- Update `CSRF_TRUSTED_ORIGINS` with your domain
- Check `ALLOWED_HOSTS` configuration

**Database Errors**
- Migrations may fail silently
- Check logs for migration errors
- Manually run: `python manage.py migrate`

**Static Files Missing**
- Ensure `collectstatic` runs in build.sh
- Check `STATIC_ROOT` and `STATICFILES_DIRS`

### File Structure
```
primefit/
├── build.sh          # Build script
├── Procfile          # Process types
├── render.yaml       # Optional: Infrastructure as Code
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
├── manage.py
├── db.sqlite3        # Will be ephemeral
├── primefit/
│   ├── settings.py   # Updated for production
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── static/       # Static files
    ├── templates/
    └── media/        # Ephemeral on free tier
```

### Production Checklist
- [ ] Set `DEBUG = False` (via environment)
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `CSRF_TRUSTED_ORIGINS`
- [ ] Use PostgreSQL for data persistence
- [ ] Configure external storage for media files
- [ ] Enable HTTPS (automatic on Render)
- [ ] Monitor logs for errors

### Free Tier Limitations
- ⏸️ Spins down after 15 min of inactivity (free web services)
- 💾 Ephemeral storage (files deleted on redeploy)
- 📊 Limited resources (512MB RAM)
- 📝 SQLite only (no persistent data between deploys)

### Recommended: Upgrade to Paid
For production use:
- Paid plan: Always running, persistent storage
- PostgreSQL database
- External media storage
- Better performance

### Support
- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com
- For issues, check Render logs in dashboard
