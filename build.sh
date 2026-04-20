#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Load demo data
python manage.py load_demo_data

# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth.models import User
import os

admin_user = os.getenv('ADMIN_USER', 'admin')
admin_email = os.getenv('ADMIN_EMAIL', 'admin@primefit.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=admin_user).exists():
    User.objects.create_superuser(admin_user, admin_email, admin_password)
    print(f"✓ Superuser '{admin_user}' created successfully!")
else:
    print(f"✓ Superuser '{admin_user}' already exists")
END

