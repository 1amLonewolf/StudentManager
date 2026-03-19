"""
Update database schema for role-based access control
Run this once to add new user fields
"""
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def update_schema():
    with app.app_context():
        # Add new columns if they don't exist
        try:
            # Try to add is_active column
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1'))
                print('✓ Added is_active column')
        except Exception as e:
            print(f'ℹ is_active column may already exist: {str(e)[:50]}')
        
        try:
            # Try to add created_by column
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN created_by INTEGER'))
                print('✓ Added created_by column')
        except Exception as e:
            print(f'ℹ created_by column may already exist: {str(e)[:50]}')
        
        # Ensure admin user exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print('✓ Default admin user created (username: admin, password: admin123)')
        else:
            print('✓ Admin user exists')
        
        # Create sample instructor if none exists
        instructor = User.query.filter_by(role='instructor').first()
        if not instructor:
            instructor = User(
                username='instructor',
                password_hash=generate_password_hash('instructor123'),
                role='instructor',
                is_active=True
            )
            db.session.add(instructor)
            db.session.commit()
            print('✓ Sample instructor created (username: instructor, password: instructor123)')
        
        # Create sample receptionist if none exists
        receptionist = User.query.filter_by(role='receptionist').first()
        if not receptionist:
            receptionist = User(
                username='receptionist',
                password_hash=generate_password_hash('receptionist123'),
                role='receptionist',
                is_active=True
            )
            db.session.add(receptionist)
            db.session.commit()
            print('✓ Sample receptionist created (username: receptionist, password: receptionist123)')
        
        print('\n✅ Database updated successfully!')
        print('\nLogin Credentials:')
        print('  Admin:       admin / admin123')
        print('  Instructor:  instructor / instructor123')
        print('  Receptionist: receptionist / receptionist123')

if __name__ == '__main__':
    update_schema()
