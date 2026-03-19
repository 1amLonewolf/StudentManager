"""
SMS Blueprint
Handles SMS notifications
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Student, SMSLog

sms_bp = Blueprint('sms', __name__, url_prefix='/sms')

@sms_bp.route('')
@login_required
def index():
    logs = SMSLog.query.order_by(SMSLog.sent_at.desc()).limit(50).all()
    return render_template('sms/index.html', logs=logs)

@sms_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    from sms_service import send_bulk_sms
    
    if request.method == 'POST':
        recipients = request.form.getlist('recipients')
        message = request.form.get('message', '')

        if not recipients or not message:
            flash('Please select recipients and enter a message', 'warning')
            return redirect(url_for('.send'))

        # Send bulk SMS
        results = send_bulk_sms(recipients, message)

        success = sum(1 for r in results if r['status'] == 'sent')
        failed = len(results) - success

        flash(f'SMS sent: {success} successful, {failed} failed', 'success' if failed == 0 else 'warning')
        return redirect(url_for('.index'))

    # Get students for recipient selection
    students = Student.query.filter_by(status='active').all()
    return render_template('sms/send.html', students=students)

@sms_bp.route('/send-reminder')
@login_required
def send_reminder():
    """Send attendance reminder to students with low attendance"""
    from sms_service import send_bulk_sms
    
    low_attendance_students = []
    for student in Student.query.filter_by(status='active').all():
        if student.attendance_rate < 70:
            low_attendance_students.append(student)

    if not low_attendance_students:
        flash('No students with low attendance found', 'info')
        return redirect(url_for('.index'))

    message = """Dear Student, your attendance is below 70%. Please attend classes regularly to complete your course successfully. - Computer Packages Course"""

    recipients = [s.phone for s in low_attendance_students if s.phone]
    results = send_bulk_sms(recipients, message)

    success = sum(1 for r in results if r['status'] == 'sent')
    flash(f'Reminder sent to {success} students with low attendance', 'success')
    return redirect(url_for('.index'))
