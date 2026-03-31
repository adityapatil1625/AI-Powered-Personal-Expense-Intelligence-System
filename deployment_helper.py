#!/usr/bin/env python3
"""
Quick script to help with deployment setup.
Generates secure tokens and validates environment.
"""

import secrets
import subprocess
import os
import sys
from pathlib import Path

def generate_secret_key():
    """Generate a secure SECRET_KEY for JWT."""
    return secrets.token_urlsafe(32)

def check_git_status():
    """Check if all changes are committed."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        if result.stdout.strip():
            print("⚠️  WARNING: Uncommitted changes found!")
            print(result.stdout)
            return False
        print("✓ All changes committed")
        return True
    except Exception as e:
        print(f"Could not check git status: {e}")
        return False

def check_requirements():
    """Check if backend requirements.txt is up to date."""
    req_path = Path(__file__).parent / "backend" / "requirements.txt"
    if req_path.exists():
        with open(req_path) as f:
            reqs = f.read()
        if all(pkg in reqs for pkg in ["fastapi", "uvicorn", "sqlalchemy", "gunicorn"]):
            print("✓ Backend requirements look good")
            return True
    print("⚠️  WARNING: Backend requirements may be incomplete")
    return False

def check_frontend_build():
    """Check if frontend can build."""
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd="frontend",
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print("✓ Frontend builds successfully")
            return True
        else:
            print("✗ Frontend build failed")
            return False
    except Exception as e:
        print(f"Could not test frontend build: {e}")
        return False

def main():
    print("=" * 60)
    print("  Expense Intelligence - Deployment Helper")
    print("=" * 60)
    print()

    # Generate SECRET_KEY
    print("\n📝 Generated Secure SECRET_KEY:")
    print("-" * 60)
    secret_key = generate_secret_key()
    print(secret_key)
    print("-" * 60)
    print("👉 Copy this value to your Render environment variables")
    print()

    # Pre-deployment checks
    print("\n🔍 Pre-Deployment Checks:")
    print("-" * 60)
    
    checks = [
        ("Git Status", check_git_status()),
        ("Backend Requirements", check_requirements()),
    ]

    all_passed = all(result for _, result in checks)
    
    print()
    if all_passed:
        print("✅ All checks passed! Ready to deploy.")
    else:
        print("⚠️  Some checks failed. Review warnings above.")
        sys.exit(1)

    # Deployment summary
    print("\n" + "=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print("""
1. Create Render account at https://render.com
2. Connect your GitHub repository
3. Create Web Service with these settings:
   - Root Directory: backend
   - Build: pip install -r requirements.txt
   - Start: gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app.main:app

4. Set Environment Variables on Render:
   - DATABASE_URL: <your-supabase-url>
   - SECRET_KEY: {secret_key}
   - CORS_ORIGIN: <your-vercel-url-later>
   - DEBUG: False

5. Deploy backend, get URL, then deploy frontend to Vercel
6. Update CORS_ORIGIN and VITE_API_URL with final URLs

See DEPLOYMENT_VERCEL_RENDER.md for detailed guide.
    """)

if __name__ == "__main__":
    main()
