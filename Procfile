web: gunicorn app.wsgi --log-file -
celery: celery worker -A app -l info -c 4
