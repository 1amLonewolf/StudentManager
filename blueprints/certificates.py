"""
Certificates Blueprint
Handles certificate generation and management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from models import db, Student, Certificate, Assessment
from datetime import datetime
import io

certificates_bp = Blueprint('certificates', __name__, url_prefix='/certificates')

@certificates_bp.route('/test-preview')
@login_required
def test_preview():
    """
    Test endpoint to preview certificate text positions
    Shows a sample certificate with position markers
    """
    from certificate_generator import generate_certificate
    
    # Get first student for testing
    student = Student.query.first()
    if not student:
        flash('No students found. Add a student first.', 'warning')
        return redirect(url_for('students.add'))
    
    # Generate test certificate
    modules_completed = ['Ms Word', 'Ms Excel', 'Ms PowerPoint']
    cert_number = 'TEST-001'
    grade = 'Distinction'
    
    try:
        output_path = generate_certificate(student, cert_number, modules_completed, grade)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        flash(f'Error generating certificate: {str(e)}', 'danger')
        return redirect(url_for('certificates.generate'))

@certificates_bp.route('')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    certificates = Certificate.query.order_by(Certificate.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('certificates/index.html', certificates=certificates)

@certificates_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    from app import generate_certificate_number
    from certificate_generator import generate_certificate
    
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
                grade = 'Pass'

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
        return redirect(url_for('.index'))

    # Get students eligible for certificates
    eligible_students = Student.query.filter(
        ((Student.status == 'completed') | (Student.status == 'active'))
    ).all()

    # Filter out those who already have certificates
    students_with_certs = Certificate.query.with_entities(Certificate.student_id).all()
    student_ids_with_certs = [c[0] for c in students_with_certs]
    eligible_students = [s for s in eligible_students if s.id not in student_ids_with_certs]

    return render_template('certificates/generate.html', students=eligible_students)

@certificates_bp.route('/<int:id>/download')
@login_required
def download(id):
    certificate = Certificate.query.get_or_404(id)
    import os
    if certificate.pdf_path and os.path.exists(certificate.pdf_path):
        return send_file(certificate.pdf_path, as_attachment=True)
    flash('Certificate file not found', 'danger')
    return redirect(url_for('.index'))

@certificates_bp.route('/<int:id>/print')
@login_required
def print(id):
    certificate = Certificate.query.get_or_404(id)
    student = Student.query.get(certificate.student_id)
    return render_template('certificates/print.html',
                         certificate=certificate,
                         student=student)
