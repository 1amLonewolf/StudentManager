from flask import Flask, jsonify
from flask_login import login_required, current_user
from flask_mail import Mail
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

from config import Config
from models import db, login_manager, migrate, User, Student, Course, Attendance, Assessment, Certificate, Payment, SMSLog, init_login_manager
from blueprints import auth_bp, main_bp, students_bp, attendance_bp, assessments_bp, certificates_bp, payments_bp, reports_bp, messaging_bp, users_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
init_login_manager(app)
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(assessments_bp)
app.register_blueprint(certificates_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(messaging_bp)
app.register_blueprint(users_bp)

# Ensure certificate output directory exists
os.makedirs(app.config['OUTPUT_CERTIFICATE_PATH'], exist_ok=True)

# ============== Context Processors ==============

@app.context_processor
def inject_config():
    """Make config values available in all templates"""
    return {
        'COURSE_FEE': app.config['COURSE_FEE'],
        'COURSE_NAME': app.config['COURSE_NAME']
    }

# ============== Helper Functions ==============

def generate_certificate_number():
    """Generate unique certificate number"""
    last_cert = Certificate.query.order_by(Certificate.id.desc()).first()
    if last_cert:
        next_num = last_cert.id + 1
    else:
        next_num = 1
    year = datetime.now().year
    return f"CERT-{year}-{next_num:04d}"

# ============== API Routes ==============

@app.route('/api/students')
@login_required
def api_students():
    students = Student.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'phone': s.phone,
        'email': s.email,
        'cohort': s.cohort,
        'status': s.status,
        'attendance_rate': s.attendance_rate,
        'average_score': s.average_score
    } for s in students])

@app.route('/api/stats')
@login_required
def api_stats():
    from models import db
    from sqlalchemy import func
    
    stats = {
        'total_students': Student.query.count(),
        'active_students': Student.query.filter_by(status='active').count(),
        'completed_students': Student.query.filter_by(status='completed').count(),
        'total_revenue': db.session.query(func.sum(Payment.amount)).scalar() or 0,
    }
    return jsonify(stats)

# ============== Database Init ==============

def create_tables():
    with app.app_context():
        db.create_all()

        # Create default admin user if not exists
        admin = User.query.filter_by(username=app.config['DEFAULT_ADMIN_USERNAME']).first()
        if not admin:
            admin = User(
                username=app.config['DEFAULT_ADMIN_USERNAME'],
                password_hash=generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD']),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print(f'Default admin created: username={app.config["DEFAULT_ADMIN_USERNAME"]}, password={app.config["DEFAULT_ADMIN_PASSWORD"]}')

        # Create default course if not exists
        course = Course.query.filter_by(name=app.config['COURSE_NAME']).first()
        if not course:
            course = Course(
                name=app.config['COURSE_NAME'],
                description='Introduction to Microsoft Office Suite and Internet',
                duration_months=app.config['COURSE_DURATION_MONTHS'],
                modules='Word,Excel,PowerPoint,Access,Publisher,Internet'
            )
            db.session.add(course)
            db.session.commit()
            print(f'Default course created: {app.config["COURSE_NAME"]}')

if __name__ == '__main__':
    create_tables()
    debug_mode = app.config.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
