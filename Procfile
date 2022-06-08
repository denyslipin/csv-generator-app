web: gunicorn app.wsgi --log-file -
worker: celery -A catalog.tasks worker -B --loglevel=info
