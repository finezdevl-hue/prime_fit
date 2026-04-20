#!/usr/bin/env python3
"""
PRIME FIT Apparels - Quick Setup Script
Run this after installing requirements:
  pip install -r requirements.txt
  python setup.py
"""
import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primefit.settings')

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"⚠  Command failed: {cmd}")
    return result.returncode

def main():
    print("\n" + "="*60)
    print("   ⚡ PRIME FIT APPARELS — Setup")
    print("="*60)

    run("python manage.py makemigrations store")
    run("python manage.py migrate")
    run("python manage.py loaddata store/fixtures/initial_data.json")

    print("\n" + "="*60)
    print("   Creating superuser for Admin Panel")
    print("="*60)
    print("\nPlease create your admin account:\n")
    run("python manage.py createsuperuser")

    print("\n" + "="*60)
    print("   ✅  Setup Complete!")
    print("="*60)
    print("""
▶  Start the server:
   python manage.py runserver

▶  Visit your site:
   http://127.0.0.1:8000/

▶  Admin Panel:
   http://127.0.0.1:8000/admin/

   Login with the superuser credentials you just created.
""")

if __name__ == '__main__':
    main()
