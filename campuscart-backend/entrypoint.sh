#!/bin/sh

# Only wait for DB if DB_HOST is explicitly set (local Docker)
if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "PostgreSQL is ready."
else
    echo "Using DATABASE_URL directly, skipping DB wait..."
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p 8000 campuscart.asgi:application
