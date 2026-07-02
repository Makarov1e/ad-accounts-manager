#!/bin/sh
set -e

echo "→ Applying database migrations..."
python manage.py migrate --noinput

echo "→ Seeding demo data (only if the table is empty)..."
python manage.py seed --if-empty --count 16

echo "→ Starting gunicorn on :8000"
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --access-logfile - \
  --error-logfile -
