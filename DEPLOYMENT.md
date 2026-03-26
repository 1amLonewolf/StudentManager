# Deployment Guide

## Local Development

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Access at: `http://localhost:5000`

---

## Production Deployment Options

### Option 1: Render (Recommended)

**Pros:**
- Free tier available
- Auto-deploy from GitHub
- PostgreSQL included
- HTTPS automatic
- Easy setup

**Cons:**
- Free tier sleeps after 15 min inactivity

#### Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Production ready"
   git push origin master
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create Web Service**
   - Click **New +** → **Web Service**
   - Connect your GitHub repository
   - Select `StudentManager`

4. **Configure Settings**
   - **Name:** `studentmanager`
   - **Region:** Oregon (closest to Kenya)
   - **Branch:** `master`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

5. **Add Environment Variables**
   - `SECRET_KEY`: Your secret key
   - `FLASK_ENV`: `production`
   - Other settings from `.env.example`

6. **Deploy**
   - Click **Create Web Service**
   - Wait 5-10 minutes for deployment

**URL:** `https://studentmanager-xxxx.onrender.com`

---

### Option 2: PythonAnywhere

**Pros:**
- Free tier (always on)
- Easy setup
- Includes database

**Cons:**
- Limited resources
- Manual deployment

#### Deploy Steps

1. **Create Account**
   - Go to https://pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Go to **Files** tab
   - Create directory: `StudentManager`
   - Upload all project files

3. **Create Virtual Environment**
   - Go to **Consoles** tab
   - Start Bash console
   - Run:
     ```bash
     cd StudentManager
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Configure Web App**
   - Go to **Web** tab
   - Click **Add a new web app**
   - Select **Manual configuration**
   - Python 3.10
   - Set paths

5. **Configure WSGI**
   Edit WSGI file:
   ```python
   import sys
   path = '/home/yourusername/StudentManager'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Set Environment Variables**
   In web tab, add:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - Other settings

7. **Reload**
   - Click **Reload** button

**URL:** `yourusername.pythonanywhere.com`

---

### Option 3: Railway

**Pros:**
- Easy deployment
- Generous free tier
- Auto-detects Python

**Cons:**
- Requires credit card for verification

#### Deploy Steps

1. **Push to GitHub** (see Render steps)

2. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

3. **Deploy**
   - Click **New Project**
   - Select **Deploy from GitHub**
   - Choose repository

4. **Configure**
   - Railway auto-detects Python
   - Set environment variables
   - Deploy

**URL:** `studentmanager.up.railway.app`

---

### Option 4: Local Network (No Internet)

**Pros:**
- Free
- Full control
- No internet required

**Cons:**
- Only accessible on your network
- Computer must stay on

#### Setup Steps

1. **Run the app**
   ```bash
   python app.py
   ```

2. **Find your IP address**
   - Windows: `ipconfig`
   - Look for IPv4 Address (e.g., 192.168.1.100)

3. **Access from other devices**
   ```
   http://YOUR_IP:5000
   ```

4. **Keep running 24/7**
   - Don't shut down computer
   - Use `launch.vbs` for auto-start on Windows boot

---

## Database Migration

### SQLite → PostgreSQL

For production deployment:

1. **Install PostgreSQL adapter**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update `.env`**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Run migrations**
   ```bash
   flask db upgrade
   ```

---

## Environment Variables

### Required for Production

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<generate-strong-key>

# Database (Render auto-configures)
DATABASE_URL=<auto-provided-by-render>

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application
COURSE_FEE=4000
COURSE_NAME=Computer Packages
COURSE_DURATION_MONTHS=2

# WhatsApp
WHATSAPP_ENABLED=true
WHATSAPP_COUNTRY_CODE=254
```

### Generate Secret Key

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Post-Deployment Checklist

- [ ] Change default admin password
- [ ] Test login
- [ ] Add test student
- [ ] Mark attendance
- [ ] Record assessment
- [ ] Generate certificate
- [ ] Test email (Gmail integration)
- [ ] Test WhatsApp
- [ ] Verify database persistence
- [ ] Set up regular backups

---

## Troubleshooting

### App Won't Start

**Check logs:**
- Render: Dashboard → Logs tab
- PythonAnywhere: Web tab → Error log

**Common issues:**
- Missing dependencies: `pip install -r requirements.txt`
- Environment variables not set
- Database connection failed

### Database Errors

**SQLite (local):**
- Delete `instance/studentmanager.db`
- Restart app

**PostgreSQL (production):**
- Check `DATABASE_URL` format
- Verify database exists
- Run migrations: `flask db upgrade`

### Email Not Working

**Gmail integration:**
- No setup needed - uses your browser
- Just click "Send via Gmail" button

**Server-side email (optional):**
- Need Gmail App Password
- Enable 2FA first
- Generate App Password at: https://myaccount.google.com/apppasswords

### Static Files Not Loading

- Clear browser cache (Ctrl+F5)
- Check file paths in templates
- Verify `static` folder uploaded

---

## Backup Strategy

### Manual Backup

**SQLite:**
```bash
# Windows
copy instance\studentmanager.db backups\studentmanager_%date%.db

# Linux/Mac
cp instance/studentmanager.db backups/studentmanager_$(date +%Y%m%d).db
```

**PostgreSQL (Render):**
- Dashboard → Database → Backups
- Download backup file

### Automated Backup

Set up weekly reminders to:
1. Export data to Excel (Reports → Export)
2. Download database backup
3. Store securely

---

## Support Resources

- **Flask Docs:** https://flask.palletsprojects.com/
- **Render Docs:** https://render.com/docs
- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Railway Docs:** https://docs.railway.app

---

**Need Help?** Contact the system administrator.
