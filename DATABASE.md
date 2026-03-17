# Database Schema

## Overview

This system uses SQLite (development) with the ability to migrate to PostgreSQL (production).

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│   User      │       │   Student        │       │   Course     │
├─────────────┤       ├──────────────────┤       ├─────────────┤
│ id          │       │ id               │       │ id          │
│ username    │       │ name             │       │ name        │
│ password    │       │ phone            │       │ description │
│ role        │       │ email            │       │ duration    │
│ created_at  │       │ id_number        │       │ modules     │
└─────────────┘       │ gender           │       │ created_at  │
                      │ enrollment_date  │       └─────────────┘
                      │ cohort           │              │
                      │ status           │              │
                      │ created_at       │              │
                      └──────────────────┘              │
                            │                           │
              ┌─────────────┼─────────────┐             │
              │             │             │             │
              ▼             ▼             ▼             ▼
    ┌────────────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
    │  Attendance    │ │Assessment│ │ Payment  │ │StudentCourse│
    ├────────────────┤ ├──────────┤ ├──────────┤ ├────────────┤
    │ id             │ │ id       │ │ id       │ │ student_id │
    │ student_id ────┼─│student_id│ │student_id│ │ course_id  │
    │ date           │ │course_id │ │ amount   │ │enrollment_ │
    │ module         │ │ module   │ │payment_  │ │   date     │
    │ present        │ │ score    │ │  date    │ │ status     │
    │ notes          │ │max_score │ │ method   │ └────────────┘
    │ recorded_at    │ │assessment│ │ reference│
    └────────────────┘ │  _type   │ │ notes    │
                       │remarks   │ │recorded_ │
                       │date_taken│ │  by      │
                       └──────────┘ └──────────┘
                            │
                            ▼
                      ┌────────────┐
                      │Certificate │
                      ├────────────┤
                      │ id         │
                      │student_id  │
                      │cert_number │
                      │issue_date  │
                      │course_name │
                      │modules     │
                      │ grade      │
                      │ pdf_path   │
                      │created_at  │
                      └────────────┘
```

## Tables Description

### User
Stores admin/instructor login credentials.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | VARCHAR(80) | Unique username |
| password_hash | VARCHAR(256) | Hashed password |
| role | VARCHAR(20) | admin or instructor |
| created_at | DATETIME | Account creation date |

### Student
Stores student personal and academic information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | Full name |
| phone | VARCHAR(20) | Phone number |
| email | VARCHAR(120) | Email address |
| id_number | VARCHAR(50) | National/Student ID |
| gender | VARCHAR(10) | Male/Female |
| enrollment_date | DATETIME | When they joined |
| cohort | VARCHAR(50) | e.g., "Jan-Mar 2026" |
| status | VARCHAR(20) | active/completed/dropped |
| created_at | DATETIME | Record creation |
| updated_at | DATETIME | Last update |

### Course
Available courses (default: Computer Packages).

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | Course name |
| description | TEXT | Course description |
| duration_months | INTEGER | Typically 2 |
| modules | VARCHAR(500) | Comma-separated modules |
| created_at | DATETIME | Creation date |

### Attendance
Daily attendance records per module.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key → Student |
| date | DATE | Attendance date |
| module | VARCHAR(50) | Word/Excel/PPT/etc. |
| present | BOOLEAN | Present or absent |
| notes | TEXT | Optional notes |
| recorded_at | DATETIME | When recorded |

**Unique Constraint**: (student_id, date, module)

### Assessment
Module assessment scores.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key → Student |
| course_id | INTEGER | Foreign key → Course |
| module | VARCHAR(50) | Word/Excel/PPT/etc. |
| score | INTEGER | Score obtained |
| max_score | INTEGER | Maximum possible |
| assessment_type | VARCHAR(50) | practical/theory/final |
| date_taken | DATETIME | Assessment date |
| remarks | TEXT | Optional remarks |

**Unique Constraint**: (student_id, module)

### Payment
Fee payment records.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key → Student |
| amount | FLOAT | Payment amount |
| payment_date | DATETIME | When paid |
| payment_method | VARCHAR(50) | cash/mpesa/bank/card |
| reference | VARCHAR(100) | Transaction reference |
| notes | TEXT | Optional notes |
| recorded_by | INTEGER | Foreign key → User |

### Certificate
Generated certificates.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key → Student |
| certificate_number | VARCHAR(50) | Unique cert number |
| issue_date | DATETIME | When issued |
| course_name | VARCHAR(100) | Course name |
| modules_completed | VARCHAR(500) | Modules passed |
| grade | VARCHAR(10) | Pass/Credit/Distinction |
| pdf_path | VARCHAR(255) | Path to PDF file |
| created_at | DATETIME | Record creation |

### SMSLog
Sent SMS message logs.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| recipient | VARCHAR(20) | Phone number |
| message | TEXT | SMS content |
| status | VARCHAR(20) | pending/sent/failed |
| sent_at | DATETIME | When sent |
| error_message | TEXT | Error if failed |

### student_courses (Junction Table)
Many-to-many relationship between students and courses.

| Column | Type | Description |
|--------|------|-------------|
| student_id | INTEGER | Foreign key → Student |
| course_id | INTEGER | Foreign key → Course |
| enrollment_date | DATETIME | When enrolled |
| status | VARCHAR(20) | active/completed/dropped |

**Primary Key**: (student_id, course_id)

## Relationships

- **User** ←→ **Payment** (one-to-many): One user can record many payments
- **Student** ←→ **Course** (many-to-many): Via student_courses junction table
- **Student** ←→ **Attendance** (one-to-many): One student has many attendance records
- **Student** ←→ **Assessment** (one-to-many): One student has many assessments
- **Student** ←→ **Payment** (one-to-many): One student has many payments
- **Student** ←→ **Certificate** (one-to-many): One student can have multiple certificates
- **Course** ←→ **Assessment** (one-to-many): One course has many assessments

## Indexes (Automatic)

- Primary keys (id) on all tables
- Foreign keys for faster joins
- Unique constraints as specified

## Sample Queries

### Get student with all data
```sql
SELECT s.*, 
       COUNT(DISTINCT a.id) as attendance_count,
       COUNT(DISTINCT asm.id) as assessment_count,
       SUM(p.amount) as total_paid
FROM Student s
LEFT JOIN Attendance a ON s.id = a.student_id
LEFT JOIN Assessment asm ON s.id = asm.student_id
LEFT JOIN Payment p ON s.id = p.student_id
WHERE s.id = 1
GROUP BY s.id;
```

### Get cohort statistics
```sql
SELECT cohort,
       COUNT(*) as total_students,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active,
       SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed
FROM Student
GROUP BY cohort;
```

### Get module pass rates
```sql
SELECT module,
       COUNT(*) as total,
       SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) as passed,
       ROUND(100.0 * SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) / COUNT(*), 2) as pass_rate
FROM Assessment
GROUP BY module;
```

## Database Location

- **Development**: `instance/studentmanager.db` (SQLite)
- **Production**: PostgreSQL connection string in `.env`

## Backup Strategy

1. **SQLite**: Copy `instance/studentmanager.db` file
2. **PostgreSQL**: Use `pg_dump` command
3. **Frequency**: Daily recommended
4. **Storage**: Off-site or cloud storage

## Migration to PostgreSQL

When ready for production:

1. Install: `pip install psycopg2-binary`
2. Create PostgreSQL database
3. Update `.env`: `DATABASE_URL=postgresql://...`
4. Run: `python app.py` (tables auto-create)
5. Migrate data (if needed)

---

**Database designed for simplicity and scalability** 🚀
