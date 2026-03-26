# COLMAC COMPUTER COLLEGE - Student Management System

A comprehensive student management system designed for COLMAC Computer College offering 2-month short courses in Microsoft Office Suite and Internet basics.

## Features

- **Student Management**: Register students, track cohorts, manage contact info
- **Attendance Tracking**: Daily attendance per module (Word, Excel, PowerPoint, Access, Publisher, Internet)
- **Assessments**: Record and track scores for each module
- **Certificates**: Generate completion certificates with student names and grades
- **Payment Tracking**: Track course fee payments and balances
- **Email Notifications**: Send emails via Gmail (browser) or default Email App
- **WhatsApp Integration**: Click-to-chat WhatsApp messaging (free)
- **Reports & Analytics**: Dashboard with stats, student reports, cohort analysis
- **Export**: Export data to Excel for external analysis

## Tech Stack

- **Backend**: Python 3.x + Flask
- **Database**: SQLite (development) → PostgreSQL (production)
- **Frontend**: HTML5 + Bootstrap 5 + Chart.js
- **PDF Generation**: ReportLab
- **Email**: Gmail web integration + mailto: links (no configuration needed)
- **WhatsApp**: Click-to-Chat (free, no API required)

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
- Configure Gmail credentials (optional - only needed for server-side email)

### 3. Initialize Database and Run

```bash
python app.py
```

The app will:
- Create the database automatically
- Set up default admin account
- Start the web server

Access at: `http://localhost:5000`

## Default Login

**Important**: Change the default password after first login!

Check your `.env` file for default credentials or contact the administrator.

## Key Features

### Certificate Requirements

Students must meet ALL three requirements to be eligible for certificate generation:

1. ✅ **Attendance ≥ 50%** - Must attend at least half of all classes
2. ✅ **Average Score ≥ 50%** - Must pass module assessments
3. ✅ **Full Payment** - Must pay complete course fee (KES 4,000)

### Email Notifications

Two options available (no server configuration needed):

1. **Send via Gmail** - Opens Gmail compose in browser with pre-filled details
2. **Open Email App** - Opens your default email client (Outlook, Mail, etc.)

Features:
- Individual student emails
- Bulk attendance alerts
- Pre-filled messages
- No SMTP configuration required

### WhatsApp Messaging

Free click-to-chat integration:
- No API required
- Uses your phone's WhatsApp
- Pre-filled messages
- Send to individual students

## Project Structure

```
StudentManager/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── models.py                   # Database models
├── forms.py                    # WTForms form classes
├── decorators.py               # Role-based access decorators
├── certificate_generator.py    # PDF certificate generation
├── email_service.py            # Email service (optional)
├── reports.py                  # Report generation & Excel export
├── commands.py                 # Flask CLI commands
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
│
├── blueprints/                 # Modular route organization
│   ├── __init__.py             # Blueprint registry
│   ├── auth.py                 # Login/logout routes
│   ├── main.py                 # Dashboard routes
│   ├── students.py             # Student CRUD routes
│   ├── attendance.py           # Attendance tracking routes
│   ├── assessments.py          # Assessment routes
│   ├── certificates.py         # Certificate generation routes
│   ├── payments.py             # Payment tracking routes
│   ├── messaging.py            # Email/WhatsApp routes
│   ├── users.py                # User management routes
│   └── reports.py              # Reports & export routes
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template with sidebar
│   ├── login.html              # Login page
│   ├── dashboard.html          # Main dashboard
│   ├── students/               # Student management templates
│   ├── attendance/             # Attendance templates
│   ├── assessments/            # Assessment templates
│   ├── certificates/           # Certificate templates
│   ├── payments/               # Payment templates
│   ├── messaging/              # Messaging templates
│   ├── reports/                # Report templates
│   └── users/                  # User management templates
│
├── static/                     # Static assets
│   ├── css/style.css           # Custom styles
│   ├── js/main.js              # JavaScript utilities
│   ├── certificates/           # Certificate templates & generated PDFs
│   └── colmac_logo.png         # College logo
│
└── Documentation
    ├── README.md               # This file
    ├── HOW_TO_RUN.md           # Quick start guide
    ├── DATABASE.md             # Database schema documentation
    ├── DEPLOYMENT.md           # Deployment instructions
    ├── MESSAGING_SETUP.md      # Email/WhatsApp setup
    ├── USER_MANAGEMENT.md      # Role-based access guide
    └── PRODUCTION_CHECKLIST.md # Production deployment checklist
```

## User Roles

### Admin
- Full system access
- User management
- All permissions

### Instructor
- Mark attendance
- Record assessments
- View student progress
- Generate certificates

### Receptionist
- Register students
- Track payments
- Manage student records

## Certificate Generation

Certificates are automatically generated with:
- Student name
- Training period (from/to dates)
- Course name (Computer Packages)
- Modules completed
- Overall grade (Pass/Credit/Distinction)
- Issue date
- Certificate number

### Grading System

- **Distinction**: 80% and above
- **Credit**: 65% - 79%
- **Pass**: 50% - 64%

## Database

### Main Tables

- **User**: System users (admin, instructors, receptionists)
- **Student**: Student records
- **Course**: Available courses
- **Attendance**: Daily attendance per module
- **Assessment**: Module scores
- **Certificate**: Generated certificates
- **Payment**: Fee payments

## Deployment

### Local Development

```bash
python app.py
```

Access at: `http://localhost:5000`

### Production (Render)

1. Push code to GitHub
2. Deploy on Render.com
3. Set environment variables
4. PostgreSQL database auto-created

See `DEPLOYMENT.md` for detailed instructions.

## Environment Variables

Required variables in `.env`:

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///studentmanager.db  # Local
# DATABASE_URL=postgresql://...           # Production

# Email (Optional - only for server-side sending)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application Settings
COURSE_FEE=4000
COURSE_NAME=Computer Packages
COURSE_DURATION_MONTHS=2

# WhatsApp
WHATSAPP_ENABLED=true
WHATSAPP_COUNTRY_CODE=254
```

## Support

For issues or questions:
- Check documentation files in the project root
- Review `HOW_TO_RUN.md` for setup help
- Check `DEPLOYMENT.md` for deployment issues

## License

Proprietary - COLMAC Computer College

## Credits

Built by [@1amLonewolf](https://github.com/1amLonewolf)
