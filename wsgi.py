"""
WSGI Entry Point for Render Deployment
"""
from app import app, create_tables
from pathlib import Path
import os

# Ensure instance directory exists
instance_path = Path(__file__).parent / 'instance'
instance_path.mkdir(exist_ok=True)

# Initialize database on startup
create_tables()

# Expose the app for gunicorn
if __name__ == "__main__":
    app.run()
