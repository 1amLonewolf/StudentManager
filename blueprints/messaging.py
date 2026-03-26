"""
Messaging Blueprint
Handles email and WhatsApp messaging
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Student, Payment
from datetime import datetime

messaging_bp = Blueprint('messaging', __name__, url_prefix='/messaging')

@messaging_bp.route('')
@login_required
def index():
    """Messaging dashboard"""
    students = Student.query.all()
    return render_template('messaging/index.html', students=students)

@messaging_bp.route('/email/<int:student_id>', methods=['GET'])
@login_required
def send_email(student_id):
    """Redirect to Gmail for sending email (server email deprecated)"""
    from flask import redirect
    
    student = Student.query.get_or_404(student_id)
    
    # Redirect to main messaging page - user should use Gmail or Email App buttons
    flash('Please use "Send via Gmail" or "Open Email App" buttons', 'info')
    return redirect(url_for('messaging.index'))

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

@messaging_bp.route('/bulk-email', methods=['GET'])
@login_required
def bulk_email():
    """Redirect to messaging page - use Gmail or Email App instead"""
    flash('Please use "Send via Gmail" or "Send via Email App" buttons for bulk emails', 'info')
    return redirect(url_for('messaging.index'))

@messaging_bp.route('/low-attendance-alerts', methods=['GET'])
@login_required
def send_low_attendance_alerts():
    """Show confirmation page for sending attendance alerts via Gmail/Email App"""
    # Get threshold from query param (default 50%)
    threshold = request.args.get('threshold', 50, type=int)

    # Get students below threshold
    low_attendance_students = [s for s in Student.query.filter_by(status='active').all() if s.attendance_rate < threshold]

    return render_template('messaging/low_attendance_confirm.html',
                         students=low_attendance_students,
                         threshold=threshold)
