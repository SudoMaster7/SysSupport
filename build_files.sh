#!/bin/bash

# Build script for Vercel
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating groups and unidades..."
python manage.py create_groups
python manage.py update_unidades

echo "Build completed!"
