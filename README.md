# Student Manager - Computer Packages Course

A simple, practical student management system designed for a computer college offering 2-month short courses in Microsoft Office Suite and Internet basics.

## Features

- **Student Management**: Register students, track cohorts, manage contact info
- **Attendance Tracking**: Daily attendance per module (Word, Excel, PowerPoint, Access, Internet)
- **Assessments**: Record and track scores for each module
- **Certificates**: Generate completion certificates with student names and grades
- **Payment Tracking**: Track course fee payments and balances
- **SMS Notifications**: Send bulk SMS to students (Twilio integration)
- **Reports & Analytics**: Dashboard with stats, student reports, cohort analysis
- **Export**: Export data to Excel for external analysis

## Tech Stack

- **Backend**: Python 3.x + Flask
- **Database**: SQLite (development) → PostgreSQL (production)
- **Frontend**: HTML5 + Bootstrap 5 + Chart.js
- **PDF Generation**: ReportLab
- **SMS**: Twilio (optional)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update settings:

```bash
cp .env.example .env
```

Edit `.env`:
- Set `SECRET_KEY` to a random string
- Configure Twilio credentials (optional, for SMS)

### 3. Initialize Database and Run

```bash
python app.py
```

The app will:
- Create the SQLite database automatically
- Create default admin user (username: `admin`, password: `admin123`)
- Create default "Computer Packages" course

### 4. Access the Application

Open your browser and go to: **http://localhost:5000**

Login with:
- **Username**: admin
- **Password**: admin123

**⚠️ Change the default password after first login!**

## Project Structure

```
StudentManager/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── forms.py                # WTForms forms
├── certificate_generator.py # PDF certificate generation
├── sms_service.py          # SMS sending service
├── reports.py              # Report generation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── static/
│   ├── css/style.css       # Custom styles
│   ├── js/main.js          # JavaScript utilities
│   └── certificates/       # Certificate templates and generated PDFs
└── templates/
    ├── base.html           # Base template
    ├── login.html          # Login page
    ├── dashboard.html      # Dashboard
    ├── students/           # Student management pages
    ├── attendance/         # Attendance pages
    ├── assessments/        # Assessment pages
    ├── certificates/       # Certificate pages
    ├── payments/           # Payment pages
    ├── sms/                # SMS pages
    └── reports/            # Report pages
```

## Usage Guide

### Adding a Student

1. Go to **Students** → **Add Student**
2. Fill in student details
3. Select cohort (e.g., "Jan-Mar 2026")
4. Save

### Marking Attendance

1. Go to **Attendance**
2. Select date and module (Word, Excel, etc.)
3. Check present/absent for each student
4. Add notes if needed
5. Save

### Recording Assessments

1. Go to **Assessments** → Select a student
2. Click **Add Assessment**
3. Select module, enter score
4. Add remarks (optional)
5. Save

### Generating Certificates

1. Ensure student has assessments recorded
2. Go to **Certificates** → **Generate Certificates**
3. Select eligible students
4. Click **Generate Selected Certificates**
5. Download or print certificates

### Custom Certificate Template

To use your college's certificate design:

1. Save your certificate as a PNG image (A4 landscape, 300 DPI recommended)
2. Place it at: `static/certificates/template.png`
3. The system will overlay student names automatically

### Sending SMS

**Development Mode** (no Twilio configured):
- Messages are logged but not sent
- Useful for testing

**Production Mode** (with Twilio):
1. Set Twilio credentials in `.env`
2. Go to **SMS** → **Send SMS**
3. Select recipients
4. Compose message
5. Send

### Exporting Data

1. Go to **Reports**
2. Choose export type (Students, Attendance, Assessments, Payments)
3. Download Excel file

## Deployment

### Local Network (Recommended for Single Computer)

```bash
python app.py
```

Access from other computers on the same network:
- Find your IP: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
- Access: `http://YOUR_IP:5000`

### Online Deployment (Free Options)

**Option 1: PythonAnywhere (Free)**
1. Create account at pythonanywhere.com
2. Upload project files
3. Configure virtual environment
4. Set up web app

**Option 2: Render (Free)**
1. Create account at render.com
2. Connect GitHub repository
3. Deploy as Web Service

**Option 3: Railway (Free)**
1. Create account at railway.app
2. Deploy from GitHub
3. Configure environment variables

## Database Backup

SQLite database is stored at: `instance/studentmanager.db`

**Backup**: Copy this file to a safe location regularly.

**Restore**: Replace the database file with your backup.

## Troubleshooting

**Port already in use:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database errors:**
```bash
# Delete and recreate database
rm instance/studentmanager.db
python app.py
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

## Security Notes

- Change default admin password immediately
- Use strong SECRET_KEY in production
- Enable HTTPS for online deployments
- Regular database backups
- Keep dependencies updated

## Future Enhancements

- Student login portal (view own progress)
- Email notifications
- QR code attendance
- Advanced analytics
- Multi-course support
- Staff management
- Library integration

## License

This project is created as a passion project for educational purposes. Feel free to modify and use as needed.

## Support

For issues or questions, check the Flask documentation:
- Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/docs/5.3/

---

**Built with ❤️ for Computer Packages Course**
