"""
Messaging Blueprint
Handles email and WhatsApp messaging
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Student, Payment, SMSLog
from datetime import datetime

messaging_bp = Blueprint('messaging', __name__, url_prefix='/messaging')

@messaging_bp.route('')
@login_required
def index():
    """Messaging dashboard"""
    students = Student.query.all()
    return render_template('messaging/index.html', students=students)

@messaging_bp.route('/email/<int:student_id>', methods=['GET', 'POST'])
@login_required
def send_email(student_id):
    """Send email to student"""
    from email_service import send_welcome_email, send_payment_receipt, send_attendance_alert, send_certificate_email, send_monthly_report
    from reports import generate_student_report
    from app import app
    
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        email_type = request.form.get('type')
        recipient_email = request.form.get('email', student.email)
        
        if not recipient_email:
            flash('No email address provided', 'warning')
            return redirect(url_for('messaging.index'))
        
        success = False
        
        if email_type == 'welcome':
            success = send_welcome_email(student, recipient_email)
        elif email_type == 'attendance':
            success = send_attendance_alert(student, recipient_email)
        elif email_type == 'report':
            report_data = generate_student_report(student, app.config['COURSE_FEE'])
            success = send_monthly_report(student, report_data, recipient_email)
        elif email_type == 'custom':
            # Custom email would need additional implementation
            flash('Custom email not implemented yet', 'info')
        
        if success:
            flash(f'Email sent to {recipient_email}', 'success')
        else:
            flash('Failed to send email. Check email configuration.', 'danger')
        
        return redirect(url_for('messaging.index'))
    
    return render_template('messaging/send_email.html', student=student)

@messaging_bp.route('/whatsapp/<int:student_id>')
@login_required
def send_whatsapp(student_id):
    """Generate WhatsApp click-to-chat link"""
    from config import Config
    
    student = Student.query.get_or_404(student_id)
    message = request.args.get('message', '')
    
    # Clean phone number
    phone = student.phone or ''
    phone = ''.join(c for c in phone if c.isdigit())
    
    # Add country code if not present
    if phone and not phone.startswith('+'):
        country_code = Config.WHATSAPP_COUNTRY_CODE
        if phone.startswith('0'):
            phone = phone[1:]  # Remove leading 0
        phone = country_code + phone
    
    # Create WhatsApp URL
    if phone:
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f'https://wa.me/{phone}?text={encoded_message}'
        return redirect(whatsapp_url)
    
    flash('No phone number for this student', 'warning')
    return redirect(url_for('students.view', id=student_id))

@messaging_bp.route('/bulk-email', methods=['POST'])
@login_required
def bulk_email():
    """Send email to multiple students"""
    from email_service import send_welcome_email, send_attendance_alert
    from app import app
    
    student_ids = request.form.getlist('student_ids')
    email_type = request.form.get('type')
    
    if not student_ids:
        flash('No students selected', 'warning')
        return redirect(url_for('messaging.index'))
    
    count = 0
    for student_id in student_ids:
        student = Student.query.get(int(student_id))
        if student and student.email:
            if email_type == 'welcome':
                send_welcome_email(student, student.email)
            elif email_type == 'attendance':
                send_attendance_alert(student, student.email)
            count += 1
    
    flash(f'Emails sent to {count} students', 'success')
    return redirect(url_for('messaging.index'))

@messaging_bp.route('/low-attendance-alerts', methods=['GET', 'POST'])
@login_required
def send_low_attendance_alerts():
    """Send attendance alerts to students with low attendance"""
    from email_service import send_attendance_alert
    import logging

    # Get threshold from query param (default 50%)
    threshold = request.args.get('threshold', 50, type=int)

    if request.method == 'POST':
        # Send alerts to students below threshold
        low_attendance_students = [s for s in Student.query.filter_by(status='active').all() if s.attendance_rate < threshold]

        count = 0
        sent_emails = []
        for student in low_attendance_students:
            if student.email:
                send_attendance_alert(student, student.email)
                count += 1
                sent_emails.append(f'{student.name} ({student.email})')

        # Log sent emails
        if sent_emails:
            logging.info(f'Attendance alerts sent to: {", ".join(sent_emails)}')
            flash(f'✅ Attendance alerts sent to {count} students:<br>' + 
                  f'<small>{"<br>".join(sent_emails)}</small>', 'success')
        else:
            flash(f'ℹ️ No students found with attendance below {threshold}%', 'info')
        
        return redirect(url_for('messaging.index'))

    # GET request - show confirmation page
    low_attendance_students = [s for s in Student.query.filter_by(status='active').all() if s.attendance_rate < threshold]

    return render_template('messaging/low_attendance_confirm.html',
                         students=low_attendance_students,
                         threshold=threshold)
