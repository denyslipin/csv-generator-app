web: gunicorn app.wsgi --log-file -
celery: celery -A app worker -l info --pool=solo
