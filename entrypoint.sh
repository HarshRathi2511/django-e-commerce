

# python manage.py migrate --no-input
# python manage.py collectstatic --no-input

# gunicorn core:wsgi:application --bind 0.0.0.0:8000



#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations main --noinput 
python manage.py migrate --noinput 

python manage.py collectstatic --noinput

gunicorn core:wsgi:application --bind 0.0.0.0:8000
exec "$@"