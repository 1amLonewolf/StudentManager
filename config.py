import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///studentmanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Certificate settings
    CERTIFICATE_TEMPLATE_PATH = os.environ.get('CERTIFICATE_TEMPLATE_PATH', 'static/certificates/template.png')
    OUTPUT_CERTIFICATE_PATH = os.environ.get('OUTPUT_CERTIFICATE_PATH', 'static/certificates/generated')
    
    # SMS settings (Twilio)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
    
    # Pagination
    STUDENTS_PER_PAGE = 10
