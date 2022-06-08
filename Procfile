web: gunicorn app.wsgi --log-file -
worker: celery worker -A app -l info
