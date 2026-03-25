"""
WSGI Entry Point for Render Deployment
"""
from app import app, create_tables

# Initialize database on startup
create_tables()

# Expose the app for gunicorn
if __name__ == "__main__":
    app.run()
