# Quick Setup Guide - Student Manager

## Step 1: Install Python

1. Go to https://python.org/downloads
2. Download Python 3.10 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

## Step 2: Verify Installation

Open Command Prompt (cmd) and run:
```bash
python --version
```

You should see: `Python 3.10.x` (or newer)

## Step 3: Install Dependencies

Navigate to the project folder and install requirements:
```bash
cd C:\Users\ADMIN\Desktop\StudentManager
python -m pip install -r requirements.txt
```

## Step 4: Run the Application

### Option A: Use the Start Script
Double-click `start.bat`

### Option B: Manual Start
```bash
python app.py
```

## Step 5: Access the Application

Open your web browser and go to:
**http://localhost:5000**

### Default Login:
- **Username**: admin
- **Password**: admin123

**⚠️ Change the password after first login!**

---

## Troubleshooting

### "python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and check "Add to PATH"
- Or use: `py -m pip install -r requirements.txt`

### "Port 5000 already in use"
Edit `app.py` line at bottom:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port to 5001
```

### "Module not found"
Run again:
```bash
python -m pip install -r requirements.txt
```

### "Database error"
Delete the instance folder and restart:
```bash
rmdir /s instance
python app.py
```

---

## First Steps After Login

1. **Add a Student**
   - Go to Students → Add Student
   - Fill in details and cohort (e.g., "Jan-Mar 2026")

2. **Mark Attendance**
   - Go to Attendance
   - Select date and module
   - Check present/absent

3. **Record Assessment**
   - Go to a student's profile
   - Click "Add Assessment"
   - Enter score for each module

4. **Generate Certificate**
   - Go to Certificates → Generate
   - Select students who completed
   - Download PDF certificates

---

## Need Help?

- Check `README.md` for detailed documentation
- Check `DEPLOYMENT.md` for online deployment
- Flask docs: https://flask.palletsprojects.com/

---

**Ready to go! 🚀**
