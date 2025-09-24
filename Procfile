web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_superuser && gunicorn business_app.wsgi:application --bind 0.0.0.0:$PORT
