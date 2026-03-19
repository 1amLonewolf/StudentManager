"""
User Management Blueprint
Admin-only user and role management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from decorators import admin_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('')
@login_required
@admin_required
def index():
    """List all users (Admin only)"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users/index.html', users=users)

@users_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    """Add new user (Admin only)"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'instructor')
        is_active = request.form.get('is_active') == 'on'
        
        # Validation
        if not username:
            flash('Username is required', 'danger')
            return redirect(url_for('.add'))
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('.add'))
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('.add'))
        
        # Create user
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role,
            is_active=is_active,
            created_by=current_user.id
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {username} created with role: {role}', 'success')
        return redirect(url_for('.index'))
    
    return render_template('users/form.html', user=None, title='Add User')

@users_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    """Edit user (Admin only)"""
    user = User.query.get_or_404(id)
    
    # Prevent editing own role/status
    is_own_profile = user.id == current_user.id
    
    if request.method == 'POST':
        # Update password if provided
        password = request.form.get('password', '')
        if password and len(password) >= 6:
            user.password_hash = generate_password_hash(password)
        
        # Update role and status (only for other users)
        if not is_own_profile:
            user.role = request.form.get('role', user.role)
            user.is_active = request.form.get('is_active') == 'on'
            
            # Save custom permissions
            user.set_permission('can_access_attendance', request.form.get('perm_attendance') == 'on')
            user.set_permission('can_access_assessments', request.form.get('perm_assessments') == 'on')
            user.set_permission('can_access_payments', request.form.get('perm_payments') == 'on')
            user.set_permission('can_access_users', request.form.get('perm_users') == 'on')
        
        db.session.commit()
        
        flash(f'User {user.username} updated successfully', 'success')
        return redirect(url_for('.index'))
    
    return render_template('users/form.html', user=user, title='Edit User', is_own_profile=is_own_profile)

@users_bp.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_status(id):
    """Activate/deactivate user (Admin only)"""
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('You cannot deactivate your own account', 'warning')
        return redirect(url_for('.index'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} {status}', 'success')
    return redirect(url_for('.index'))

@users_bp.route('/<int:id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_password(id):
    """Reset user password (Admin only)"""
    user = User.query.get_or_404(id)
    
    # Generate temporary password
    import random, string
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    user.password_hash = generate_password_hash(temp_password)
    db.session.commit()
    
    flash(f'Password reset for {user.username}. Temporary password: {temp_password}', 'info')
    return redirect(url_for('.index'))

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Edit own profile"""
    if request.method == 'POST':
        # Update password if provided
        password = request.form.get('password', '')
        if password and len(password) >= 6:
            current_user.password_hash = generate_password_hash(password)
            db.session.commit()
            flash('Password updated successfully', 'success')
        elif password:
            flash('Password must be at least 6 characters', 'danger')
        
        return redirect(url_for('.profile'))
    
    return render_template('users/profile.html')

@users_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change own password"""
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('.profile'))
    
    if not new_password or len(new_password) < 6:
        flash('New password must be at least 6 characters', 'danger')
        return redirect(url_for('.profile'))
    
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Password changed successfully', 'success')
    return redirect(url_for('.profile'))
