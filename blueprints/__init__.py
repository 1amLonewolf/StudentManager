"""
Blueprints Package
Organizes routes into modular components
"""
from .auth import auth_bp
from .main import main_bp
from .students import students_bp
from .attendance import attendance_bp
from .assessments import assessments_bp
from .certificates import certificates_bp
from .payments import payments_bp
from .reports import reports_bp
from .messaging import messaging_bp
from .users import users_bp

__all__ = [
    'auth_bp',
    'main_bp',
    'students_bp',
    'attendance_bp',
    'assessments_bp',
    'certificates_bp',
    'payments_bp',
    'reports_bp',
    'messaging_bp',
    'users_bp'
]
