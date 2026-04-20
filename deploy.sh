#!/bin/bash
# Deploy to Render - Quick Start

echo "🚀 PRIME FIT Render Deployment Checklist"
echo "======================================"
echo ""

# Check required files
echo "✓ Checking required files..."
required_files=("build.sh" "Procfile" "runtime.txt" ".env.example" "requirements.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file MISSING - please create it"
    fi
done

echo ""
echo "📋 Deployment Steps:"
echo "1. Create .env file from .env.example:"
echo "   cp .env.example .env"
echo "   # Edit .env with your values"
echo ""
echo "2. Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Render deployment'"
echo "   git push"
echo ""
echo "3. On Render Dashboard:"
echo "   - Create new Web Service"
echo "   - Connect GitHub repo"
echo "   - Build Command: bash build.sh"
echo "   - Start Command: gunicorn primefit.wsgi:application --bind 0.0.0.0:\$PORT"
echo "   - Add environment variables from .env"
echo ""
echo "4. Deploy"
echo "   - Push to GitHub automatically triggers deploy"
echo "   - Check Render logs for errors"
echo ""
echo "📊 Key Configuration Files:"
echo "  • build.sh       - Build script (pip, collectstatic, migrate)"
echo "  • Procfile       - Process file (web dyno)"
echo "  • runtime.txt    - Python version"
echo "  • requirements.txt - Dependencies with gunicorn, whitenoise"
echo "  • .env.example   - Environment variables template"
echo ""
echo "🔐 Required Environment Variables:"
echo "  • DEBUG (False for production)"
echo "  • SECRET_KEY (strong random key)"
echo "  • DJANGO_ALLOWED_HOSTS (your domain)"
echo "  • DATABASE_URL (sqlite or PostgreSQL)"
echo "  • CSRF_TRUSTED_ORIGINS (https://your-domain)"
echo ""
echo "⚠️  Important Notes:"
echo "  • Free tier: ephemeral storage (files lost on redeploy)"
echo "  • Media files are NOT preserved between deploys"
echo "  • Use external storage (S3, Cloudinary) for production"
echo "  • Static files handled by WhiteNoise"
echo ""
echo "✅ Deployment complete!"
