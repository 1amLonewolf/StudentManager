# Production Deployment Checklist

## Before Deploying Online

### 🔒 Security
- [ ] Generate a strong `SECRET_KEY` (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Change default admin password immediately after first login
- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Never commit `.env` file to git

### 📦 Dependencies
- [ ] Run `pip install -r requirements.txt` to verify all packages install correctly
- [ ] Gunicorn is included for production server

### 🗄️ Database
- [ ] Test with SQLite locally (already working)
- [ ] For production: Consider PostgreSQL for better performance
- [ ] Backup your database regularly

### 📧 Email Setup
- [ ] Get Gmail App Password: https://myaccount.google.com/apppasswords
- [ ] Test email sending before going live
- [ ] Add your email to `.env`:
  ```
  MAIL_USERNAME=your-email@gmail.com
  MAIL_PASSWORD=your-app-password
  MAIL_DEFAULT_SENDER=your-email@gmail.com
  ```

### 📱 WhatsApp/SMS
- [ ] Set correct country code for WhatsApp (default: 254 for Kenya)
- [ ] SMS via Twilio is optional (paid service)

### 🎓 Certificates
- [ ] Create certificate template image at `static/certificates/template.png`
- [ ] Test certificate generation with sample student

### 🧪 Testing
- [ ] Test login with default credentials (admin/admin123)
- [ ] Add a test student
- [ ] Mark attendance
- [ ] Record assessment
- [ ] Generate certificate
- [ ] Test payment tracking
- [ ] Test email notifications
- [ ] Test WhatsApp messaging

---

## Deployment Options

### Option 1: PythonAnywhere (Recommended for Beginners)
**Pros:** Free, easy setup, includes database
**Cons:** Limited resources on free tier

1. Create account at https://pythonanywhere.com
2. Upload files via Files tab
3. Create virtualenv and install dependencies
4. Configure web app in Web tab
5. Reload and test

**URL:** `yourusername.pythonanywhere.com`

### Option 2: Render (Recommended)
**Pros:** Free tier, auto-deploy from GitHub, modern platform
**Cons:** Free tier sleeps after 15 min inactivity

1. Push code to GitHub
2. Create account at https://render.com
3. Deploy from GitHub repository
4. Set environment variables
5. Deploy

**URL:** `student-manager.onrender.com`

### Option 3: Railway
**Pros:** Easy deployment, generous free tier
**Cons:** Requires credit card for verification

1. Push to GitHub
2. Deploy from GitHub at https://railway.app
3. Set environment variables

### Option 4: Local Network (No Internet Required)
**Pros:** Free, full control, no internet needed
**Cons:** Only accessible on your network

1. Run `python app.py`
2. Access from other devices: `http://YOUR_IP:5000`
3. Keep computer running 24/7 for constant access

---

## After Deployment

### Immediate Actions
1. Login with default credentials
2. Go to Users → Change admin password
3. Test all major features
4. Add real students and data

### Ongoing Maintenance
- [ ] Backup database weekly (download `instance/studentmanager.db`)
- [ ] Monitor disk space (certificates accumulate)
- [ ] Check error logs regularly
- [ ] Update dependencies periodically

### Troubleshooting

**App won't start:**
- Check environment variables are set correctly
- Verify `requirements.txt` installed without errors
- Check logs on your hosting platform

**Database errors:**
- Delete `instance/studentmanager.db` and restart (local only)
- For production, check DATABASE_URL format

**Email not sending:**
- Verify Gmail App Password (not regular password)
- Check "Less secure app access" or use App Password
- Test with `MAIL_ADMIN` email first

**Static files not loading:**
- Clear browser cache
- Check file paths are correct
- Verify `static` folder uploaded correctly

---

## Quick Deploy Commands

### Local Testing
```bash
pip install -r requirements.txt
python app.py
```

### Deploy to Render
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/studentmanager.git
git push -u origin main
# Then deploy on Render.com from GitHub
```

### Backup Database
```bash
# Windows
copy instance\studentmanager.db backups\studentmanager_%date%.db

# Linux/Mac
cp instance/studentmanager.db backups/studentmanager_$(date +%Y%m%d).db
```

---

## Support Resources
- Flask Docs: https://flask.palletsprojects.com/
- Render Docs: https://render.com/docs
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Gmail App Password: https://support.google.com/accounts/answer/185833
