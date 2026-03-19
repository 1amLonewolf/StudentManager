"""
Flask CLI Commands
Run with: flask command
"""
from app import app, db
from models import User, Student, Course, Attendance, Assessment
from werkzeug.security import generate_password_hash
import click

@app.cli.command("init-db")
@click.option("--drop", is_flag=True, help="Drop existing tables first")
def init_db(drop):
    """Initialize the database."""
    if drop:
        click.echo("Dropping existing tables...")
        db.drop_all()
    
    click.echo("Creating tables...")
    db.create_all()
    
    # Create default admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        
        # Create default course
        course = Course(
            name='Computer Packages',
            description='Introduction to Microsoft Office Suite and Internet',
            duration_months=2,
            modules='Word,Excel,PowerPoint,Access,Publisher,Internet'
        )
        db.session.add(course)
        db.session.commit()
        
        click.echo("Default admin created: admin / admin123")
        click.echo("Default course created: Computer Packages")
    else:
        click.echo("Database already initialized.")
    
    click.echo("Database initialized successfully!")

@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
@click.option("--role", default="admin", help="User role")
def create_admin(username, password, role):
    """Create a new admin user."""
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo(f"Error: User '{username}' already exists!")
        return
    
    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    click.echo(f"Admin user '{username}' created successfully!")

@app.cli.command("reset-admin-password")
@click.argument("new_password")
def reset_admin_password(new_password):
    """Reset the admin password."""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        click.echo("Error: Admin user not found!")
        return
    
    admin.password_hash = generate_password_hash(new_password)
    db.session.commit()
    click.echo("Admin password reset successfully!")

@app.cli.command("stats")
def show_stats():
    """Show database statistics."""
    click.echo("\n=== Database Statistics ===\n")
    click.echo(f"Students: {Student.query.count()}")
    click.echo(f"Users: {User.query.count()}")
    click.echo(f"Courses: {Course.query.count()}")
    click.echo(f"Attendance Records: {Attendance.query.count()}")
    click.echo(f"Assessments: {Assessment.query.count()}")
    click.echo("")
