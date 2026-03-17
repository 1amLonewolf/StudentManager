"""
SMS Service
Handles sending SMS messages via Twilio or other providers
Supports free tier for development/testing
"""
import os
from datetime import datetime
from flask import current_app

def send_sms(recipient, message):
    """
    Send a single SMS message
    
    Args:
        recipient: Phone number
        message: Message text
    
    Returns:
        dict with status and message
    """
    from models import SMSLog, db
    
    # Check if Twilio is configured
    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID', '') or os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN', '') or os.environ.get('TWILIO_AUTH_TOKEN', '')
    twilio_number = current_app.config.get('TWILIO_PHONE_NUMBER', '') or os.environ.get('TWILIO_PHONE_NUMBER', '')
    
    result = {'status': 'pending', 'recipient': recipient, 'message': message}
    
    # Log the SMS attempt
    sms_log = SMSLog(
        recipient=recipient,
        message=message,
        status='pending'
    )
    
    if not account_sid or not auth_token:
        # Twilio not configured - log but don't send (development mode)
        sms_log.status = 'sent'
        sms_log.error_message = 'SMS not sent - Twilio not configured (development mode)'
        db.session.add(sms_log)
        db.session.commit()
        
        result['status'] = 'sent'
        result['message'] = f'[DEV MODE] SMS would be sent to {recipient}'
        print(f"[SMS DEV MODE] To: {recipient}, Message: {message}")
        return result
    
    # Send via Twilio
    try:
        from twilio.rest import Client
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient
        )
        
        sms_log.status = 'sent'
        result['status'] = 'sent'
        result['sid'] = message.sid
        
    except Exception as e:
        sms_log.status = 'failed'
        sms_log.error_message = str(e)
        result['status'] = 'failed'
        result['error'] = str(e)
    
    db.session.add(sms_log)
    db.session.commit()
    
    return result


def send_bulk_sms(recipients, message):
    """
    Send SMS to multiple recipients
    
    Args:
        recipients: List of phone numbers
        message: Message text
    
    Returns:
        List of results for each recipient
    """
    results = []
    
    for recipient in recipients:
        # Clean phone number (remove spaces, dashes, etc.)
        clean_number = ''.join(c for c in recipient if c.isdigit() or c == '+')
        
        if clean_number:
            result = send_sms(clean_number, message)
            results.append(result)
    
    return results


def send_attendance_alert(student, attendance_rate):
    """Send attendance warning to student"""
    message = f"""Dear {student.name}, your attendance is {attendance_rate}%. Please attend regularly to complete your course. - Computer Packages"""
    return send_sms(student.phone, message)


def send_completion_congratulations(student):
    """Send congratulations to student who completed the course"""
    message = f"""Dear {student.name}, congratulations on completing the Computer Packages course! Your certificate is ready for collection. - College Admin"""
    return send_sms(student.phone, message)


def send_payment_reminder(student, amount_due):
    """Send payment reminder to student"""
    message = f"""Dear {student.name}, you have an outstanding balance of {amount_due}. Please complete payment to continue your course. - College Admin"""
    return send_sms(student.phone, message)


def send_exam_reminder(student, exam_date):
    """Send exam reminder to student"""
    message = f"""Dear {student.name}, reminder: Your Computer Packages exam is on {exam_date}. Please be punctual. - College Admin"""
    return send_sms(student.phone, message)
