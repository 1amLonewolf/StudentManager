# 🚀 How to Run Student Manager

## ⚡ Quick Start (Choose ONE method)

### Method 1: Double-click `launch.vbs` (RECOMMENDED)
- **File**: `launch.vbs`
- **What it does**: Opens app in a new window that stays open
- **Best for**: Daily use

### Method 2: Use `run.bat`
- **File**: `run.bat`
- **What it does**: Simple batch launcher
- **Best for**: When you want to see console output

### Method 3: Manual (Most Reliable)
1. Open Command Prompt
2. Run these commands:
```bash
cd C:\Users\ADMIN\Desktop\StudentManager
venv\Scripts\activate
python app.py
```

---

## 🌐 Access the Application

Once running, open your browser to:
**http://localhost:5000**

### Login:
- **Username**: admin
- **Password**: admin123

---

## ❓ Why Did start.bat Close Immediately?

Windows batch files can close instantly if:
1. Python isn't in PATH
2. Virtual environment doesn't exist
3. Dependencies aren't installed
4. There's an error in the script

**Solution**: Use `launch.vbs` or Method 3 (manual) above.

---

## 🔧 First Time Setup

If running for the first time:

```bash
cd C:\Users\ADMIN\Desktop\StudentManager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 🛑 How to Stop

- **If using .vbs or .bat**: Close the command window
- **If using manual**: Press `Ctrl+C` in the Command Prompt

---

## ✅ Verify It's Running

1. Look for this message:
   ```
   * Running on http://127.0.0.1:5000
   ```

2. Open browser to: http://localhost:5000

3. You should see the login page

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python from https://python.org
- Check "Add Python to PATH" during installation

### "Module not found"
```bash
cd C:\Users\ADMIN\Desktop\StudentManager
venv\Scripts\activate
pip install -r requirements.txt
```

### "Port 5000 in use"
Edit `app.py`, change last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### App opens then closes immediately
- Use `launch.vbs` instead of `start.bat`
- Or use Method 3 (manual commands)

---

## 📋 File Checklist

Make sure these exist:
- ✅ `app.py` - Main application
- ✅ `venv/` - Virtual environment folder
- ✅ `instance/` - Database folder (created automatically)
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS/JS files

---

## 💡 Tips

1. **Keep the command window open** while using the app
2. **Bookmark** http://localhost:5000 in your browser
3. **Change password** after first login!
4. **Backup** `instance/studentmanager.db` regularly

---

**Need Help?** Check `README.md` or `SUCCESS.md`
