# Deployment Guide

## Local Development (Already Working!)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Access at: http://localhost:5000

---

## Deploy to PythonAnywhere (Free)

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Sign up for free account

### Step 2: Upload Files
1. Go to **Files** tab
2. Create directory: `StudentManager`
3. Upload all project files

### Step 3: Create Virtual Environment
1. Go to **Consoles** tab
2. Start Bash console
3. Run:
```bash
cd StudentManager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Python 3.10 (or latest)
5. Set source code directory to: `/home/yourusername/StudentManager`
6. Set virtualenv to: `/home/yourusername/StudentManager/venv`

### Step 5: Configure WSGI
Edit WSGI configuration file:
```python
import sys
path = '/home/yourusername/StudentManager'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 6: Set Environment Variables
In **Web** → **WSGI configuration file**:
```python
import os
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['DATABASE_URL'] = 'sqlite:///studentmanager.db'
```

### Step 7: Reload
Click **Reload** button on Web tab

**Your app is now live at:** `yourusername.pythonanywhere.com`

---

## Deploy to Render (Free)

### Step 1: Prepare for Render

Create `render.yaml`:
```yaml
services:
  - type: web
    name: student-manager
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        generateValue: true
```

### Step 2: Push to GitHub
1. Create GitHub repository
2. Push your code

### Step 3: Deploy on Render
1. Go to https://render.com
2. Sign up/Login
3. **New +** → **Web Service**
4. Connect GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables
7. Deploy

**Your app is now live at:** `student-manager.onrender.com`

---

## Deploy to Railway (Free)

### Step 1: Create Railway Account
Go to https://railway.app

### Step 2: Deploy from GitHub
1. Click **New Project**
2. Select **Deploy from GitHub**
3. Choose your repository

### Step 3: Configure
Railway auto-detects Python apps. Just set environment variables:
- `SECRET_KEY`
- `DATABASE_URL`

### Step 4: Deploy
Click **Deploy**

**Your app is now live!**

---

## Production Checklist

- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Set up regular database backups
- [ ] Configure Twilio for SMS (optional)
- [ ] Add certificate template
- [ ] Test all features
- [ ] Document admin credentials securely

---

## Database Migration (SQLite → PostgreSQL)

For production deployment:

### 1. Install PostgreSQL adapter
```bash
pip install psycopg2-binary
```

### 2. Update `.env`
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 3. Update `models.py` (if needed)
SQLite is mostly compatible with PostgreSQL, but for production consider using Flask-Migrate:

```bash
pip install Flask-Migrate
```

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Database locked"
Delete `instance/studentmanager.db` and restart:
```bash
python app.py
```

### Static files not loading
Check `static` folder permissions and ensure paths are correct.

---

## Need Help?

- Flask Docs: https://flask.palletsprojects.com/
- PythonAnywhere Forums: https://help.pythonanywhere.com/
- Render Docs: https://render.com/docs
