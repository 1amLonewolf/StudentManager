"""
Payments Blueprint
Handles fee payment tracking (Receptionist/Admin only)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Student, Payment
from sqlalchemy import func
from decorators import receptionist_required

payments_bp = Blueprint('payments', __name__, url_prefix='/payments', template_folder='../templates')

@payments_bp.route('')
@login_required
@receptionist_required
def index():
    from app import app
    
    page = request.args.get('page', 1, type=int)
    payments = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    # Calculate stats
    total_revenue = db.session.query(func.sum(Payment.amount)).scalar() or 0
    COURSE_FEE = app.config['COURSE_FEE']
    pending_fees = 0
    for student in Student.query.filter_by(status='active').all():
        pending = COURSE_FEE - student.total_paid
        if pending > 0:
            pending_fees += pending

    return render_template('payments/index.html',
                         payments=payments,
                         total_revenue=total_revenue,
                         pending_fees=pending_fees)

@payments_bp.route('/students/<int:id>', methods=['GET', 'POST'])
@login_required
def student_payments(id):
    from forms import PaymentForm
    
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
        return redirect(url_for('.student_payments', id=student.id))

    return render_template('payments/student_payments.html',
                         student=student,
                         form=form,
                         payments=student.payments)
