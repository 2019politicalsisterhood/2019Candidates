web: gunicorn config.wsgi:application
worker: celery worker --app=political_sisterhood.taskapp --loglevel=info
