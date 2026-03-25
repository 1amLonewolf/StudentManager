#!/usr/bin/env bash
# Post-build script for Render

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import create_tables; create_tables()"

echo "Database initialized successfully!"
