import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Use the provided DATABASE_URL (for PostgreSQL or custom SQLite path)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Use SQLite in instance folder with absolute path
        instance_path = Path(__file__).parent / 'instance'
        instance_path.mkdir(exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{instance_path}/studentmanager.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application settings
    COURSE_FEE = int(os.environ.get('COURSE_FEE', 4000))  # Course fee in KES
    COURSE_NAME = os.environ.get('COURSE_NAME', 'Computer Packages')
    COURSE_DURATION_MONTHS = int(os.environ.get('COURSE_DURATION_MONTHS', 2))
    
    # Default admin credentials (change in production!)
    DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin123')

    # Email settings (Gmail SMTP - Free)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 'yes']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')  # Your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')  # Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', '')  # Usually same as MAIL_USERNAME
    MAIL_ADMIN = os.environ.get('MAIL_ADMIN', '')  # Admin email for notifications

    # WhatsApp settings (Click-to-Chat - Free)
    WHATSAPP_ENABLED = os.environ.get('WHATSAPP_ENABLED', 'true').lower() in ['true', '1', 'yes']
    WHATSAPP_COUNTRY_CODE = os.environ.get('WHATSAPP_COUNTRY_CODE', '254')  # Default: Kenya

    # Certificate settings
    CERTIFICATE_TEMPLATE_PATH = os.environ.get('CERTIFICATE_TEMPLATE_PATH', 'static/certificates/template.png')
    OUTPUT_CERTIFICATE_PATH = os.environ.get('OUTPUT_CERTIFICATE_PATH', 'static/certificates/generated')
    COLLEGE_LOGO_PATH = os.environ.get('COLLEGE_LOGO_PATH', 'static/colmac_logo.png')

    # SMS settings (Twilio - Optional, paid)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')

    # Pagination
    STUDENTS_PER_PAGE = int(os.environ.get('STUDENTS_PER_PAGE', 10))
