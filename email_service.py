"""
Email Service
Handles all email notifications using Flask-Mail
Free tier: Gmail SMTP (500 emails/day)
"""
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
import os

def send_async_email(app, msg):
    """Send email asynchronously to avoid blocking"""
    with app.app_context():
        try:
            from app import mail
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Email send error: {str(e)}')
            return False

def send_email(subject, recipients, text_body, html_body):
    """
    Send email to one or more recipients
    
    Args:
        subject: Email subject
        recipients: List of email addresses or single string
        text_body: Plain text version
        html_body: HTML version (optional)
    
    Returns:
        bool: True if sent successfully
    """
    if not current_app.config.get('MAIL_USERNAME'):
        current_app.logger.info('Email not configured - skipping send')
        return False
    
    if isinstance(recipients, str):
        recipients = [recipients]
    
    msg = Message(
        subject,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=recipients
    )
    msg.body = text_body
    msg.html = html_body
    
    # Send asynchronously
    from app import app
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    
    current_app.logger.info(f'Email queued to {recipients}')
    return True

# ============== Email Templates ==============

def send_welcome_email(student, student_email):
    """Send welcome email to new student"""
    subject = f'Welcome to {current_app.config["COURSE_NAME"]}!'
    
    text_body = f'''Dear {student.name},

Welcome to {current_app.config["COURSE_NAME"]} course!

We're excited to have you join us. Your enrollment has been confirmed with the following details:

Student Name: {student.name}
Cohort: {student.cohort}
Enrollment Date: {student.enrollment_date.strftime('%d %B %Y')}
Course Duration: {current_app.config["COURSE_DURATION_MONTHS"]} months

Course Modules:
- Microsoft Word
- Microsoft Excel
- Microsoft PowerPoint
- Microsoft Access
- Microsoft Publisher
- Internet Basics

If you have any questions, please don't hesitate to contact us.

Best regards,
Course Administrator
{current_app.config["COURSE_NAME"]}
'''
    
    html_body = render_template(
        'emails/welcome.html',
        student=student,
        course_name=current_app.config['COURSE_NAME'],
        duration=current_app.config['COURSE_DURATION_MONTHS']
    )
    
    return send_email(subject, student_email, text_body, html_body)

def send_payment_receipt(student, payment, recipient_email):
    """Send payment receipt email"""
    subject = f'Payment Receipt - {student.name}'
    
    text_body = f'''Dear {student.name},

Thank you for your payment. Here are the details:

Payment Amount: KES {payment.amount}
Payment Date: {payment.payment_date.strftime('%d %B %Y')}
Payment Method: {payment.payment_method.capitalize()}
Reference: {payment.reference or 'N/A'}

Total Paid: KES {student.total_paid}
Pending Balance: KES {max(0, current_app.config['COURSE_FEE'] - student.total_paid)}

Best regards,
Accounts Department
'''
    
    html_body = render_template(
        'emails/payment_receipt.html',
        student=student,
        payment=payment,
        course_fee=current_app.config['COURSE_FEE']
    )
    
    return send_email(subject, recipient_email, text_body, html_body)

def send_attendance_alert(student, recipient_email):
    """Send low attendance alert email"""
    subject = f'Attendance Alert - {student.name}'

    # Calculate attendance stats
    classes_attended = sum(1 for a in student.attendances if a.present)
    total_classes = len(student.attendances)

    text_body = f'''Dear {student.name},

This is to inform you that your current attendance rate is {student.attendance_rate}%, which is below the required 50%.

Please attend classes regularly to complete your course successfully and qualify for your certificate.

Current Statistics:
- Attendance Rate: {student.attendance_rate}%
- Minimum Required: 50%
- Classes Attended: {classes_attended}
- Total Classes: {total_classes}

If you have any challenges affecting your attendance, please contact the administration.

Best regards,
Course Administrator
'''

    html_body = render_template(
        'emails/attendance_alert.html',
        student=student,
        classes_attended=classes_attended,
        total_classes=total_classes
    )

    return send_email(subject, recipient_email, text_body, html_body)

def send_certificate_email(student, certificate, recipient_email):
    """Send certificate email with PDF attachment"""
    subject = f'Your Certificate - {student.name}'
    
    text_body = f'''Dear {student.name},

Congratulations on completing the {current_app.config["COURSE_NAME"]} course!

Your certificate is ready. Please find it attached to this email.

Certificate Details:
- Certificate Number: {certificate.certificate_number}
- Grade: {certificate.grade}
- Issue Date: {certificate.issue_date.strftime('%d %B %Y')}

We wish you all the best in your future endeavors!

Best regards,
Course Administrator
'''
    
    html_body = render_template(
        'emails/certificate_ready.html',
        student=student,
        certificate=certificate
    )
    
    # Note: Attachment would need to be added in the send_email function
    # For now, we'll send with download link
    return send_email(subject, recipient_email, text_body, html_body)

def send_monthly_report(student, report_data, recipient_email):
    """Send monthly progress report email"""
    subject = f'Monthly Progress Report - {student.name}'
    
    text_body = f'''Dear {student.name},

Here is your monthly progress report for {current_app.config["COURSE_NAME"]}:

Attendance:
- Rate: {report_data['attendance']['rate']}%
- Present: {report_data['attendance']['present_days']} days
- Absent: {report_data['attendance']['absent_days']} days

Performance:
- Average Score: {report_data['performance']['average_score']}%
- Grade: {report_data['performance']['grade']}
- Modules Passed: {report_data['performance']['modules_passed']}/{report_data['performance']['modules_total']}

Payment Status:
- Total Paid: KES {report_data['payments']['total_paid']}
- Pending: KES {report_data['payments']['pending']}

Keep up the good work!

Best regards,
Course Administrator
'''
    
    html_body = render_template(
        'emails/monthly_report.html',
        student=student,
        report=report_data
    )
    
    return send_email(subject, recipient_email, text_body, html_body)
