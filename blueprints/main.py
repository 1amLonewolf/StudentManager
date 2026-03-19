"""
Main Blueprint
Handles dashboard and main pages
"""
from flask import Blueprint, render_template
from flask_login import login_required
from models import Student, Payment, Attendance, Assessment
from sqlalchemy import func
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    from app import app, db
    
    stats = {
        'total_students': Student.query.count(),
        'active_students': Student.query.filter_by(status='active').count(),
        'completed_students': Student.query.filter_by(status='completed').count(),
        'total_revenue': db.session.query(func.sum(Payment.amount)).scalar() or 0,
        'pending_fees': 0,
        'attendance_rate': 0,
        'pass_rate': 0,
    }

    # Calculate pending fees
    COURSE_FEE = app.config['COURSE_FEE']
    for student in Student.query.filter_by(status='active').all():
        pending = COURSE_FEE - student.total_paid
        if pending > 0:
            stats['pending_fees'] += pending

    # Average attendance rate
    attendances = Attendance.query.all()
    if attendances:
        present = sum(1 for a in attendances if a.present)
        stats['attendance_rate'] = round((present / len(attendances)) * 100, 1)

    # Pass rate (students with average score >= 50%)
    students_with_assessments = Student.query.join(Assessment).distinct().all()
    passed = sum(1 for s in students_with_assessments if s.average_score >= 50)
    if students_with_assessments:
        stats['pass_rate'] = round((passed / len(students_with_assessments)) * 100, 1)

    # Recent students
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()

    # Upcoming completions
    two_months_ago = datetime.now() - timedelta(days=60)
    upcoming_completions = Student.query.filter(
        Student.enrollment_date <= two_months_ago,
        Student.status == 'active'
    ).all()

    return render_template('dashboard.html',
                         stats=stats,
                         recent_students=recent_students,
                         upcoming_completions=upcoming_completions)
