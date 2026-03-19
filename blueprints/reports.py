"""
Reports Blueprint
Handles reports and data export
"""
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required
from models import db, Student, Course, Payment
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('')
@login_required
def index():
    from app import app
    
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

    students = Student.query.all()
    cohorts = db.session.query(Student.cohort).distinct().filter(Student.cohort != None).all()
    cohorts = [c[0] for c in cohorts if c[0]]
    
    return render_template('reports/index.html',
                         stats=stats,
                         students=students,
                         cohorts=cohorts)

@reports_bp.route('/student/<int:id>')
@login_required
def student(id):
    from reports import generate_student_report
    from app import app
    
    student = Student.query.get_or_404(id)
    report_data = generate_student_report(student, course_fee=app.config['COURSE_FEE'])
    return render_template('reports/student.html', student=student, report=report_data)

@reports_bp.route('/cohort')
@login_required
def cohort():
    from reports import generate_cohort_report
    
    cohort = request.args.get('cohort', '')
    report_data = generate_cohort_report(cohort)
    cohorts = db.session.query(Student.cohort).distinct().filter(Student.cohort != None).all()
    cohorts = [c[0] for c in cohorts if c[0]]
    return render_template('reports/cohort.html', report=report_data, cohorts=cohorts, selected_cohort=cohort)

@reports_bp.route('/export')
@login_required
def export():
    from reports import export_to_excel
    from datetime import datetime
    
    export_type = request.args.get('type', 'students')
    output = export_to_excel(export_type)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'{export_type}_export_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )
