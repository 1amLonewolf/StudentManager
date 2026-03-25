"""
Reset admin user script
Run this once to delete old 'admin' user and ensure 'Colmac' exists
"""
from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Delete old admin user
    old_admin = User.query.filter_by(username='admin').first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
        print('✅ Old admin user deleted')
    
    # Create or update Colmac user
    colmac = User.query.filter_by(username='Colmac').first()
    if not colmac:
        colmac = User(
            username='Colmac',
            password_hash=generate_password_hash('Colmac@2026!Secure#StudentMgr'),
            role='admin',
            active=True
        )
        db.session.add(colmac)
        db.session.commit()
        print('✅ New Colmac admin user created')
    else:
        # Update password if user exists
        colmac.password_hash = generate_password_hash('Colmac@2026!Secure#StudentMgr')
        colmac.role = 'admin'
        colmac.active = True
        db.session.commit()
        print('✅ Colmac password updated')
    
    # Show all users
    users = User.query.all()
    print('\n📋 Current users:')
    for u in users:
        print(f'  - {u.username} ({u.role})')
    
    print('\n✅ Done! You can now login with:')
    print('   Username: Colmac')
    print('   Password: Colmac@2026!Secure#StudentMgr')
