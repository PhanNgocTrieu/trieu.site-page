#!/bin/bash
set -e

echo "=== Spiritual Feed Startup ==="

# Wait for database to be ready (using Python instead of psql for Neon compatibility)
echo "Waiting for database..."
python -c "
import time
import sys
from sqlalchemy import create_engine
import os

db_url = os.environ.get('DATABASE_URL')
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        engine = create_engine(db_url)
        conn = engine.connect()
        conn.close()
        print('Database connection successful!')
        sys.exit(0)
    except Exception as e:
        retry_count += 1
        print(f'Database unavailable (attempt {retry_count}/{max_retries}), waiting...')
        time.sleep(2)

print('Failed to connect to database after maximum retries')
sys.exit(1)
"

echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
flask db upgrade

# Conditional seeding based on environment
if [ "$APP_ENV" = "dev" ]; then
    echo "Development environment detected - checking for seed data..."
    python -c "
from app import create_app
from app.models.user import User
from app.extensions import db

app = create_app()
with app.app_context():
    # Check if we need to seed
    user_count = User.query.count()
    if user_count <= 1:  # Only admin exists or empty
        print('Seeding development data...')
        try:
            import seed_posts
            print('Development data seeded successfully')
        except Exception as e:
            print(f'Seed failed (non-critical): {e}')
    else:
        print(f'Database already has {user_count} users, skipping seed')
"
fi

# Create default admin (idempotent)
echo "Ensuring default admin user exists..."
python init_admin.py

echo "=== Starting Gunicorn Server ==="
exec gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app
