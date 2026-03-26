# StudentManager - Project Summary

## Overview

A comprehensive web-based student management system for COLMAC Computer College, designed for 2-month Computer Packages courses.

## Current Status

✅ **Production Ready** - Deployed and operational

## Core Features

### 1. Student Management
- Student registration with full details
- Cohort tracking
- Contact information management
- ID number tracking
- Status management (active/completed/dropped)

### 2. Attendance Tracking
- Daily attendance per module
- Modules: Word, Excel, PowerPoint, Access, Publisher, Internet
- Attendance rate calculation
- Low attendance alerts (< 50%)

### 3. Assessments
- Module-based scoring
- Multiple assessment types (practical, theory, final)
- Automatic grade calculation
- Pass/fail tracking per module

### 4. Certificate Generation
- PDF certificates with official template
- Auto-generated certificate numbers
- Grade-based classification (Pass/Credit/Distinction)
- **Requirements enforced:**
  - Attendance ≥ 50%
  - Average score ≥ 50%
  - Full fee payment (KES 4,000)

### 5. Payment Tracking
- Course fee management
- Partial payment support
- Balance calculation
- Payment method tracking (cash, M-Pesa, bank, card)

### 6. Notifications
- **Email:** Gmail web integration + mailto links (no configuration)
- **WhatsApp:** Click-to-Chat (free, no API)
- Bulk attendance alerts
- Pre-filled message templates

### 7. Reports & Analytics
- Dashboard with key metrics
- Student performance reports
- Cohort analysis
- Excel export functionality
- Chart.js visualizations

### 8. User Management
- Role-based access control
- Three roles: Admin, Instructor, Receptionist
- Custom permissions support
- User activity tracking

## Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **Language:** Python 3.x
- **ORM:** SQLAlchemy 2.0
- **Database:** 
  - Development: SQLite
  - Production: PostgreSQL (Render)

### Frontend
- **UI Framework:** Bootstrap 5.3.2
- **Icons:** Bootstrap Icons 1.11.1
- **Charts:** Chart.js 4.4.0
- **Templates:** Jinja2

### Libraries
- **PDF Generation:** ReportLab 4.0.7
- **Excel Export:** openpyxl 3.1.2
- **Image Processing:** Pillow >=10.0.0
- **Forms:** Flask-WTF 1.2.1
- **Authentication:** Flask-Login 0.6.3
- **Migrations:** Flask-Migrate 4.0.5
- **Production Server:** Gunicorn

## Project Structure

```
StudentManager/
├── app.py                          # Main application entry point
├── config.py                       # Configuration management
├── models.py                       # SQLAlchemy models
├── forms.py                        # WTForms classes
├── decorators.py                   # Access control decorators
├── certificate_generator.py        # PDF certificate generation
├── email_service.py                # Email service (optional)
├── reports.py                      # Report generation
├── commands.py                     # CLI commands
│
├── blueprints/                     # Route organization
│   ├── auth.py                     # Authentication
│   ├── main.py                     # Dashboard
│   ├── students.py                 # Student CRUD
│   ├── attendance.py               # Attendance tracking
│   ├── assessments.py              # Assessment management
│   ├── certificates.py             # Certificate generation
│   ├── payments.py                 # Payment tracking
│   ├── messaging.py                # Email/WhatsApp
│   ├── users.py                    # User management
│   └── reports.py                  # Reports & exports
│
├── templates/                      # HTML templates
│   ├── base.html                   # Master template
│   ├── login.html                  # Login page
│   ├── dashboard.html              # Dashboard
│   └── [feature]/                  # Feature-specific templates
│
├── static/                         # Static assets
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript files
│   ├── certificates/               # Certificate templates
│   └── colmac_logo.png             # College logo
│
└── Documentation/
    ├── README.md                   # Main documentation
    ├── HOW_TO_RUN.md               # Quick start guide
    ├── DATABASE.md                 # Database schema
    ├── DEPLOYMENT.md               # Deployment guide
    ├── MESSAGING_SETUP.md          # Email/WhatsApp setup
    ├── USER_MANAGEMENT.md          # User roles guide
    └── PRODUCTION_CHECKLIST.md     # Production checklist
```

## Database Schema

### Core Tables

1. **User**
   - System authentication
   - Roles: admin, instructor, receptionist
   - Custom permissions support

2. **Student**
   - Personal information
   - Enrollment details
   - Status tracking
   - Relationships: attendances, assessments, payments, certificates

3. **Course**
   - Course details
   - Default: Computer Packages
   - Duration: 2 months

4. **Attendance**
   - Daily records per module
   - Present/absent status
   - Date and module tracking

5. **Assessment**
   - Module scores
   - Assessment types
   - Pass/fail calculation

6. **Certificate**
   - Generated certificates
   - Certificate numbers
   - Grade tracking
   - PDF storage

7. **Payment**
   - Fee payments
   - Payment methods
   - Balance tracking
   - Recorded by user

## Key Workflows

### Student Enrollment
1. Add student via Students → Add Student
2. Fill in personal details
3. Select cohort and enrollment date
4. Optional: Send welcome email/WhatsApp

### Daily Operations
1. Mark attendance by date and module
2. Record assessments as students complete modules
3. Track payments as fees are received

### End of Course
1. Verify certificate eligibility:
   - Attendance ≥ 50%
   - Average score ≥ 50%
   - Full payment
2. Generate certificates
3. Export reports to Excel
4. Send completion notifications

## Access Control

### Admin
- Full system access
- User management
- All permissions
- Can override restrictions

### Instructor
- Mark attendance
- Record assessments
- View student progress
- Generate certificates
- Cannot: Manage users, access payments

### Receptionist
- Register students
- Track payments
- Manage student records
- Cannot: Mark attendance, record assessments

## Certificate Requirements

All THREE requirements must be met:

| Requirement | Threshold | Enforced At |
|-------------|-----------|-------------|
| **Attendance** | ≥ 50% | Generation + Download |
| **Average Score** | ≥ 50% | Generation |
| **Full Payment** | KES 4,000 | Generation + Download |

## Deployment

### Local Development
```bash
pip install -r requirements.txt
python app.py
```
Access: `http://localhost:5000`

### Production (Render)
- Auto-deploy from GitHub
- PostgreSQL database
- Gunicorn web server
- Environment variables configured

## Security

- Password hashing (Werkzeug)
- Session management (Flask-Login)
- CSRF protection (Flask-WTF)
- Role-based access control
- Environment variable separation
- No hardcoded credentials in production

## Performance Optimizations

- Database indexes on frequently queried columns
- Eager loading for relationships
- Pagination for large datasets
- Efficient SQL queries
- Static asset CDN usage

## Future Enhancements

Potential improvements:
- Student portal (self-service)
- Parent portal (view child's progress)
- Mobile app
- Advanced analytics
- Automated backup system
- Multi-course support
- Online fee payment integration

## Support & Maintenance

### Regular Tasks
- Weekly database backups
- Monitor disk space (certificates)
- Check error logs
- Update dependencies quarterly

### Troubleshooting
- Check documentation files
- Review application logs
- Verify environment variables
- Test database connectivity

## Credits

**Developer:** [@1amLonewolf](https://github.com/1amLonewolf)  
**Client:** COLMAC Computer College  
**Version:** 1.0 (Production)  
**License:** Proprietary

---

**Last Updated:** March 2026
