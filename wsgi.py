"""
WSGI Entry Point for Render Deployment
"""
from app import app, create_tables
from models import db
from flask_migrate import Migrate
import os

# Initialize database
with app.app_context():
    try:
        # Try to create tables (works for SQLite)
        db.create_all()
    except Exception as e:
        # For PostgreSQL, tables should be created via migrations
        app.logger.info(f"Tables may already exist: {e}")

# Expose the app for gunicorn
if __name__ == "__main__":
    app.run()
