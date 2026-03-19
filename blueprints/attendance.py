"""
Attendance Blueprint
Handles attendance tracking (Instructor/Admin only)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Student, Attendance
from datetime import datetime
from decorators import instructor_required

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance', template_folder='../templates')

@attendance_bp.route('')
@login_required
@instructor_required
def index():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    module = request.args.get('module', 'Word')

    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    modules = ['Word', 'Excel', 'PowerPoint', 'Access', 'Publisher', 'Internet']

    # Get all active students
    students = Student.query.filter_by(status='active').all()

    # Get existing attendance records for this date/module
    existing = {}
    for record in Attendance.query.filter_by(date=date_obj, module=module).all():
        existing[record.student_id] = record

    return render_template('attendance/index.html',
                         students=students,
                         date=date,
                         module=module,
                         modules=modules,
                         existing=existing)

@attendance_bp.route('/save', methods=['POST'])
@login_required
def save():
    date_str = request.form.get('date')
    module = request.form.get('module')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Process each student's attendance
    student_ids = request.form.getlist('student_ids')
    for student_id in student_ids:
        present = request.form.get(f'present_{student_id}') is not None
        notes = request.form.get(f'notes_{student_id}', '')

        # Upsert attendance record
        record = Attendance.query.filter_by(
            student_id=int(student_id),
            date=date_obj,
            module=module
        ).first()

        if record:
            record.present = present
            record.notes = notes
        else:
            record = Attendance(
                student_id=int(student_id),
                date=date_obj,
                module=module,
                present=present,
                notes=notes
            )
            db.session.add(record)

    db.session.commit()
    flash('Attendance saved successfully!', 'success')
    return redirect(url_for('.index', date=date_str, module=module))

@attendance_bp.route('/history')
@login_required
def history():
    student_id = request.args.get('student_id', type=int)

    if student_id:
        student = Student.query.get_or_404(student_id)
        records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
        return render_template('attendance/history.html', records=records, student=student)

    return redirect(url_for('students.index'))
