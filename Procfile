web: gunicorn app.wsgi --log-file -
worker: celery -A app worker -l info --pool=solo
