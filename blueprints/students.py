"""
Students Blueprint
Handles student CRUD operations
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Student, Course
from datetime import datetime

students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('')
@login_required
def index():
    from app import app
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

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    from forms import StudentForm
    
    # Get courses for dropdown
    courses = Course.query.all()
    if not courses:
        # Create default course if none exists
        default_course = Course(
            name='Computer Packages',
            description='Introduction to Microsoft Office Suite and Internet',
            duration_months=2,
            modules='Word,Excel,PowerPoint,Access,Publisher,Internet'
        )
        db.session.add(default_course)
        db.session.commit()
        courses = [default_course]

    form = StudentForm()
    form.course_id.choices = [(c.id, c.name) for c in courses]

    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            id_number=form.id_number.data,
            gender=form.gender.data,
            cohort=form.cohort.data,
            enrollment_date=form.enrollment_date.data
        )

        # Assign to course
        if form.course_id.data:
            course = Course.query.get(form.course_id.data)
            student.courses.append(course)

        db.session.add(student)
        db.session.commit()

        flash(f'Student {student.name} added successfully!', 'success')
        return redirect(url_for('.index'))

    return render_template('students/form.html', form=form, courses=courses, title='Add Student')

@students_bp.route('/<int:id>')
@login_required
def view(id):
    student = Student.query.get_or_404(id)
    return render_template('students/view.html', student=student)

@students_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    from forms import StudentForm
    
    student = Student.query.get_or_404(id)
    courses = Course.query.all()
    form = StudentForm(obj=student)
    form.course_id.choices = [(c.id, c.name) for c in courses]

    if form.validate_on_submit():
        student.name = form.name.data
        student.phone = form.phone.data
        student.email = form.email.data
        student.id_number = form.id_number.data
        student.gender = form.gender.data
        student.cohort = form.cohort.data
        student.enrollment_date = form.enrollment_date.data
        student.status = form.status.data

        db.session.commit()
        flash(f'Student {student.name} updated successfully!', 'success')
        return redirect(url_for('.view', id=student.id))

    return render_template('students/form.html', form=form, courses=courses, title='Edit Student', student=student)

@students_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {student.name} deleted successfully!', 'success')
    return redirect(url_for('.index'))
