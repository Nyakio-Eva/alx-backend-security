web: gunicorn backend_security.wsgi:application --log-file -
worker: celery -A backend_security worker -l info
beat: celery -A backend_security beat -l info
