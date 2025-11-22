#!/bin/bash

echo "Starting Django application..."

# Install dependencies (optional if using GitHub Actions)
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Start Gunicorn 
gunicorn perfume_shop.wsgi:application \
    --bind=0.0.0.0:$PORT \
    --workers=4 \
    --timeout=600 \
    --access-logfile '-' \
    --error-logfile '-'
