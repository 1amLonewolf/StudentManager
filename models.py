from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Association table for students and courses (many-to-many)
student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=datetime.utcnow),
    db.Column('status', db.String(20), default='active')  # active, completed, dropped
)

class User(UserMixin, db.Model):
    """Admin/Instructor users with role-based access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='instructor')  # admin, instructor, receptionist
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Custom permissions (JSON format)
    # Example: {"can_access_attendance": true, "can_access_payments": false}
    custom_permissions = db.Column(db.Text, default='{}')

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_instructor(self):
        return self.role in ['admin', 'instructor']
    
    @property
    def is_receptionist(self):
        return self.role in ['admin', 'receptionist']
    
    def get_permissions(self):
        """Get custom permissions as dict"""
        import json
        try:
            return json.loads(self.custom_permissions or '{}')
        except:
            return {}
    
    def set_permission(self, key, value):
        """Set a specific permission"""
        import json
        perms = self.get_permissions()
        perms[key] = value
        self.custom_permissions = json.dumps(perms)
    
    def has_permission(self, key):
        """Check if user has specific permission"""
        perms = self.get_permissions()
        return perms.get(key, False)

class Course(db.Model):
    """Available courses (e.g., Computer Packages)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_months = db.Column(db.Integer, default=2)
    modules = db.Column(db.String(500))  # Comma-separated: Word,Excel,PPT,Access,Internet
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', secondary=student_courses, 
                               backref=db.backref('courses', lazy='dynamic'))
    assessments = db.relationship('Assessment', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Student(db.Model):
    """Student records"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    id_number = db.Column(db.String(50))  # National ID or student ID
    gender = db.Column(db.String(10))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    cohort = db.Column(db.String(50))  # e.g., "Jan-Mar 2026"
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='student', lazy=True, cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='student', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='student', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments)
    
    @property
    def attendance_rate(self):
        if not self.attendances:
            return 0
        present = sum(1 for a in self.attendances if a.present)
        return round((present / len(self.attendances)) * 100, 1)
    
    @property
    def average_score(self):
        if not self.assessments:
            return 0
        scores = [a.score for a in self.assessments if a.score]
        return round(sum(scores) / len(scores), 1) if scores else 0
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Attendance(db.Model):
    """Daily attendance records"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    module = db.Column(db.String(50))  # Word, Excel, PPT, Access, Internet
    present = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'date', 'module', name='unique_attendance'),)
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.date} - {self.module}>'

class Assessment(db.Model):
    """Module assessments/scores"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    module = db.Column(db.String(50), nullable=False)  # Word, Excel, PPT, Access, Internet
    score = db.Column(db.Integer)  # Out of 100
    max_score = db.Column(db.Integer, default=100)
    assessment_type = db.Column(db.String(50), default='practical')  # practical, theory, final
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    remarks = db.Column(db.Text)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'module', name='unique_assessment_module'),)
    
    @property
    def percentage(self):
        if not self.score or not self.max_score:
            return 0
        return round((self.score / self.max_score) * 100, 1)
    
    @property
    def passed(self):
        return self.percentage >= 50
    
    def __repr__(self):
        return f'<Assessment {self.student_id} - {self.module} - {self.score}>'

class Certificate(db.Model):
    """Generated certificates"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    course_name = db.Column(db.String(100))
    modules_completed = db.Column(db.String(500))  # Comma-separated list
    grade = db.Column(db.String(10))  # Pass, Credit, Distinction
    pdf_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number} - {self.student_id}>'

class Payment(db.Model):
    """Fee payment tracking"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))  # cash, mpesa, bank, etc.
    reference = db.Column(db.String(100))  # Transaction reference
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Payment {self.student_id} - {self.amount}>'

# Initialize login_manager
def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
