"""
Assessments Blueprint
Handles student assessments and scores
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Student, Assessment, Course

assessments_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessments_bp.route('')
@login_required
def index():
    student_id = request.args.get('student_id', type=int)

    if student_id:
        student = Student.query.get_or_404(student_id)
        return render_template('assessments/index.html',
                             student=student,
                             assessments=student.assessments)

    return redirect(url_for('students.index'))

@assessments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    from forms import AssessmentForm
    
    # Get student for context
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id) if student_id else None
    courses = Course.query.all()

    form = AssessmentForm()
    form.course_id.choices = [(c.id, c.name) for c in courses]

    if form.validate_on_submit():
        # Check if assessment already exists for this student/module
        existing = Assessment.query.filter_by(
            student_id=form.student_id.data,
            module=form.module.data
        ).first()

        if existing:
            flash(f'Assessment for {form.module.data} already exists for this student!', 'warning')
            return redirect(url_for('.index', student_id=form.student_id.data))

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
        return redirect(url_for('.index', student_id=form.student_id.data))

    return render_template('assessments/form.html', form=form, student=student, courses=courses)

@assessments_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    assessment = Assessment.query.get_or_404(id)
    student_id = assessment.student_id
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('.index', student_id=student_id))
