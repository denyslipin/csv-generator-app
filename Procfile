web: gunicorn app.wsgi --log-file -
celery -A app worker -l info --pool=solo
