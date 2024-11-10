#!/bin/sh

# Exec make migrations
echo "Making migrations..."
python manage.py makemigrations

# Exec migrate Django
echo "Applying migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run server in the background
echo "Starting server on 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000