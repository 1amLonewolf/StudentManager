from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import io

from config import Config
from models import db, login_manager, User, Student, Course, Attendance, Assessment, Certificate, Payment, SMSLog, init_login_manager
from forms import LoginForm, StudentForm, AttendanceForm, AssessmentForm, PaymentForm
from certificate_generator import generate_certificate
from sms_service import send_sms, send_bulk_sms
from reports import generate_student_report, generate_cohort_report, export_to_excel

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
init_login_manager(app)

# Ensure certificate output directory exists
os.makedirs(app.config['OUTPUT_CERTIFICATE_PATH'], exist_ok=True)

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

def get_dashboard_stats():
    """Get analytics data for dashboard"""
    stats = {
        'total_students': Student.query.count(),
        'active_students': Student.query.filter_by(status='active').count(),
        'completed_students': Student.query.filter_by(status='completed').count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).scalar() or 0,
        'pending_fees': 0,
        'attendance_rate': 0,
        'pass_rate': 0,
    }
    
    # Calculate pending fees (assuming course fee is 10000, adjust as needed)
    COURSE_FEE = 10000
    for student in Student.query.filter_by(status='active').all():
        pending = COURSE_FEE - student.total_paid
        if pending > 0:
            stats['pending_fees'] += pending
    
    # Average attendance rate
    attendances = Attendance.query.all()
    if attendances:
        present = sum(1 for a in attendances if a.present)
        stats['attendance_rate'] = round((present / len(attendances)) * 100, 1)
    
    # Pass rate (students with average score >= 50%)
    students_with_assessments = Student.query.join(Assessment).distinct().all()
    passed = sum(1 for s in students_with_assessments if s.average_score >= 50)
    if students_with_assessments:
        stats['pass_rate'] = round((passed / len(students_with_assessments)) * 100, 1)
    
    return stats

# ============== Auth Routes ==============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ============== Dashboard ==============

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    stats = get_dashboard_stats()
    
    # Recent students
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    # Upcoming completions (enrolled 2 months ago)
    two_months_ago = datetime.now() - timedelta(days=60)
    upcoming_completions = Student.query.filter(
        Student.enrollment_date <= two_months_ago,
        Student.status == 'active'
    ).all()
    
    # Monthly enrollment trend (last 6 months)
    from sqlalchemy import func
    six_months_ago = datetime.now() - timedelta(days=180)
    enrollment_trend = db.session.query(
        func.strftime('%Y-%m', Student.enrollment_date),
        db.func.count(Student.id)
    ).filter(Student.enrollment_date >= six_months_ago).group_by(
        func.strftime('%Y-%m', Student.enrollment_date)
    ).all()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_students=recent_students,
                         upcoming_completions=upcoming_completions,
                         enrollment_trend=enrollment_trend)

# ============== Student Routes ==============

@app.route('/students')
@login_required
def students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Student.query
    
    if search:
        query = query.filter(Student.name.ilike(f'%{search}%'))
    if status:
        query = query.filter_by(status=status)
    
    students = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=app.config['STUDENTS_PER_PAGE'], error_out=False
    )
    
    return render_template('students/index.html', students=students, search=search, status=status)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    
    # Get courses for dropdown
    courses = Course.query.all()
    if not courses:
        # Create default course if none exists
        default_course = Course(
            name='Computer Packages',
            description='Introduction to Microsoft Office Suite and Internet',
            duration_months=2,
            modules='Word,Excel,PowerPoint,Access,Internet'
        )
        db.session.add(default_course)
        db.session.commit()
        courses = [default_course]
    
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            id_number=form.id_number.data,
            gender=form.gender.data,
            cohort=form.cohort.data,
            enrollment_date=datetime.now()
        )
        
        # Assign to course
        if form.course_id.data:
            course = Course.query.get(form.course_id.data)
            student.courses.append(course)
        
        db.session.add(student)
        db.session.commit()
        
        flash(f'Student {student.name} added successfully!', 'success')
        return redirect(url_for('students'))
    
    return render_template('students/form.html', form=form, courses=courses, title='Add Student')

@app.route('/students/<int:id>')
@login_required
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('students/view.html', student=student)

@app.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    courses = Course.query.all()
    
    if form.validate_on_submit():
        student.name = form.name.data
        student.phone = form.phone.data
        student.email = form.email.data
        student.id_number = form.id_number.data
        student.gender = form.gender.data
        student.cohort = form.cohort.data
        student.status = form.status.data
        
        db.session.commit()
        flash(f'Student {student.name} updated successfully!', 'success')
        return redirect(url_for('view_student', id=student.id))
    
    return render_template('students/form.html', form=form, courses=courses, title='Edit Student', student=student)

@app.route('/students/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {student.name} deleted successfully!', 'success')
    return redirect(url_for('students'))

# ============== Attendance Routes ==============

@app.route('/attendance')
@login_required
def attendance():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    module = request.args.get('module', 'Word')
    
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    modules = ['Word', 'Excel', 'PowerPoint', 'Access', 'Internet']
    
    # Get all active students
    students = Student.query.filter_by(status='active').all()
    
    # Get existing attendance records for this date/module
    existing = {}
    for record in Attendance.query.filter_by(date=date_obj, module=module).all():
        existing[record.student_id] = record
    
    return render_template('attendance/index.html', 
                         students=students, 
                         date=date, 
                         module=module,
                         modules=modules,
                         existing=existing)

@app.route('/attendance/save', methods=['POST'])
@login_required
def save_attendance():
    date_str = request.form.get('date')
    module = request.form.get('module')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Process each student's attendance
    student_ids = request.form.getlist('student_ids')
    for student_id in student_ids:
        present = request.form.get(f'present_{student_id}') is not None
        notes = request.form.get(f'notes_{student_id}', '')
        
        # Upsert attendance record
        record = Attendance.query.filter_by(
            student_id=int(student_id), 
            date=date_obj, 
            module=module
        ).first()
        
        if record:
            record.present = present
            record.notes = notes
        else:
            record = Attendance(
                student_id=int(student_id),
                date=date_obj,
                module=module,
                present=present,
                notes=notes
            )
            db.session.add(record)
    
    db.session.commit()
    flash('Attendance saved successfully!', 'success')
    return redirect(url_for('attendance', date=date_str, module=module))

@app.route('/attendance/history')
@login_required
def attendance_history():
    student_id = request.args.get('student_id', type=int)
    
    if student_id:
        student = Student.query.get_or_404(student_id)
        records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
        return render_template('attendance/history.html', records=records, student=student)
    
    return redirect(url_for('students'))

# ============== Assessment Routes ==============

@app.route('/assessments')
@login_required
def assessments():
    student_id = request.args.get('student_id', type=int)
    
    if student_id:
        student = Student.query.get_or_404(student_id)
        return render_template('assessments/index.html', 
                             student=student, 
                             assessments=student.assessments)
    
    return redirect(url_for('students'))

@app.route('/assessments/add', methods=['GET', 'POST'])
@login_required
def add_assessment():
    form = AssessmentForm()
    
    if form.validate_on_submit():
        # Check if assessment already exists for this student/module
        existing = Assessment.query.filter_by(
            student_id=form.student_id.data,
            module=form.module.data
        ).first()
        
        if existing:
            flash(f'Assessment for {form.module.data} already exists for this student!', 'warning')
            return redirect(url_for('assessments', student_id=form.student_id.data))
        
        assessment = Assessment(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            module=form.module.data,
            score=form.score.data,
            max_score=form.max_score.data,
            assessment_type=form.assessment_type.data,
            remarks=form.remarks.data
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        flash('Assessment recorded successfully!', 'success')
        return redirect(url_for('assessments', student_id=form.student_id.data))
    
    # Get student for context
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id) if student_id else None
    courses = Course.query.all()
    
    return render_template('assessments/form.html', form=form, student=student, courses=courses)

@app.route('/assessments/<int:id>/delete', methods=['POST'])
@login_required
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    student_id = assessment.student_id
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('assessments', student_id=student_id))

# ============== Certificate Routes ==============

@app.route('/certificates')
@login_required
def certificates():
    page = request.args.get('page', 1, type=int)
    certificates = Certificate.query.order_by(Certificate.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('certificates/index.html', certificates=certificates)

@app.route('/certificates/generate', methods=['GET', 'POST'])
@login_required
def generate_certificate_page():
    if request.method == 'POST':
        student_ids = request.form.getlist('student_ids')
        generated = []
        
        for student_id in student_ids:
            student = Student.query.get(int(student_id))
            if not student:
                continue
            
            # Check if certificate already exists
            existing = Certificate.query.filter_by(student_id=student.id).first()
            if existing:
                flash(f'Certificate already exists for {student.name}', 'warning')
                continue
            
            # Get modules completed (from assessments)
            modules_completed = [a.module for a in student.assessments if a.passed]
            
            # Determine grade
            avg_score = student.average_score
            if avg_score >= 80:
                grade = 'Distinction'
            elif avg_score >= 65:
                grade = 'Credit'
            elif avg_score >= 50:
                grade = 'Pass'
            else:
                grade = 'Pass'  # Still pass if completed
            
            # Generate certificate
            cert_number = generate_certificate_number()
            pdf_path = generate_certificate(
                student=student,
                certificate_number=cert_number,
                modules_completed=modules_completed,
                grade=grade
            )
            
            # Save to database
            certificate = Certificate(
                student_id=student.id,
                certificate_number=cert_number,
                course_name='Computer Packages',
                modules_completed=','.join(modules_completed),
                grade=grade,
                pdf_path=pdf_path
            )
            
            db.session.add(certificate)
            generated.append(student.name)
        
        db.session.commit()
        
        if generated:
            flash(f'Certificates generated for: {", ".join(generated)}', 'success')
        return redirect(url_for('certificates'))
    
    # Get students eligible for certificates (completed or active with assessments)
    eligible_students = Student.query.filter(
        ((Student.status == 'completed') | (Student.status == 'active'))
    ).all()
    
    # Filter out those who already have certificates
    students_with_certs = Certificate.query.with_entities(Certificate.student_id).all()
    student_ids_with_certs = [c[0] for c in students_with_certs]
    eligible_students = [s for s in eligible_students if s.id not in student_ids_with_certs]
    
    return render_template('certificates/generate.html', students=eligible_students)

@app.route('/certificates/<int:id>/download')
@login_required
def download_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    if certificate.pdf_path and os.path.exists(certificate.pdf_path):
        return send_file(certificate.pdf_path, as_attachment=True)
    flash('Certificate file not found', 'danger')
    return redirect(url_for('certificates'))

@app.route('/certificates/<int:id>/print')
@login_required
def print_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    student = Student.query.get(certificate.student_id)
    return render_template('certificates/print.html', 
                         certificate=certificate, 
                         student=student)

# ============== Payment Routes ==============

@app.route('/payments')
@login_required
def payments():
    page = request.args.get('page', 1, type=int)
    payments = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Calculate stats
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    COURSE_FEE = 10000
    pending_fees = 0
    for student in Student.query.filter_by(status='active').all():
        pending = COURSE_FEE - student.total_paid
        if pending > 0:
            pending_fees += pending
    
    return render_template('payments/index.html', 
                         payments=payments,
                         total_revenue=total_revenue,
                         pending_fees=pending_fees)

@app.route('/students/<int:id>/payments', methods=['GET', 'POST'])
@login_required
def student_payments(id):
    student = Student.query.get_or_404(id)
    form = PaymentForm()
    
    if form.validate_on_submit():
        payment = Payment(
            student_id=student.id,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            reference=form.reference.data,
            notes=form.notes.data,
            recorded_by=current_user.id
        )
        
        db.session.add(payment)
        db.session.commit()
        
        flash(f'Payment of {form.amount.data} recorded successfully!', 'success')
        return redirect(url_for('student_payments', id=student.id))
    
    return render_template('payments/student_payments.html', 
                         student=student, 
                         form=form,
                         payments=student.payments)

# ============== SMS Routes ==============

@app.route('/sms')
@login_required
def sms():
    logs = SMSLog.query.order_by(SMSLog.sent_at.desc()).limit(50).all()
    return render_template('sms/index.html', logs=logs)

@app.route('/sms/send', methods=['GET', 'POST'])
@login_required
def send_sms_page():
    if request.method == 'POST':
        recipients = request.form.getlist('recipients')
        message = request.form.get('message', '')
        
        if not recipients or not message:
            flash('Please select recipients and enter a message', 'warning')
            return redirect(url_for('send_sms_page'))
        
        # Send bulk SMS
        results = send_bulk_sms(recipients, message)
        
        success = sum(1 for r in results if r['status'] == 'sent')
        failed = len(results) - success
        
        flash(f'SMS sent: {success} successful, {failed} failed', 'success' if failed == 0 else 'warning')
        return redirect(url_for('sms'))
    
    # Get students for recipient selection
    students = Student.query.filter_by(status='active').all()
    return render_template('sms/send.html', students=students)

@app.route('/sms/send-reminder')
@login_required
def send_attendance_reminder():
    """Send attendance reminder to students with low attendance"""
    low_attendance_students = []
    for student in Student.query.filter_by(status='active').all():
        if student.attendance_rate < 70:
            low_attendance_students.append(student)
    
    if not low_attendance_students:
        flash('No students with low attendance found', 'info')
        return redirect(url_for('sms'))
    
    message = """Dear Student, your attendance is below 70%. Please attend classes regularly to complete your course successfully. - Computer Packages Course"""
    
    recipients = [s.phone for s in low_attendance_students if s.phone]
    results = send_bulk_sms(recipients, message)
    
    success = sum(1 for r in results if r['status'] == 'sent')
    flash(f'Reminder sent to {success} students with low attendance', 'success')
    return redirect(url_for('sms'))

# ============== Reports Routes ==============

@app.route('/reports')
@login_required
def reports():
    stats = get_dashboard_stats()
    students = Student.query.all()
    cohorts = db.session.query(Student.cohort).distinct().filter(Student.cohort != None).all()
    cohorts = [c[0] for c in cohorts if c[0]]
    return render_template('reports/index.html', 
                         stats=stats,
                         students=students,
                         cohorts=cohorts)

@app.route('/reports/student/<int:id>')
@login_required
def student_report(id):
    student = Student.query.get_or_404(id)
    report_data = generate_student_report(student)
    return render_template('reports/student.html', student=student, report=report_data)

@app.route('/reports/cohort')
@login_required
def cohort_report():
    cohort = request.args.get('cohort', '')
    report_data = generate_cohort_report(cohort)
    cohorts = db.session.query(Student.cohort).distinct().filter(Student.cohort != None).all()
    cohorts = [c[0] for c in cohorts if c[0]]
    return render_template('reports/cohort.html', report=report_data, cohorts=cohorts, selected_cohort=cohort)

@app.route('/reports/export')
@login_required
def export_data():
    export_type = request.args.get('type', 'students')
    output = export_to_excel(export_type)
    
    from flask import send_file
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'{export_type}_export_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )

# ============== API Routes (for future scaling) ==============

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
    return jsonify(get_dashboard_stats())

# ============== Database Init ==============

def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Default admin created: username=admin, password=admin123')
        
        # Create default course if not exists
        course = Course.query.filter_by(name='Computer Packages').first()
        if not course:
            course = Course(
                name='Computer Packages',
                description='Introduction to Microsoft Office Suite and Internet',
                duration_months=2,
                modules='Word,Excel,PowerPoint,Access,Internet'
            )
            db.session.add(course)
            db.session.commit()
            print('Default course created: Computer Packages')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
