export DJANGO_SETTINGS_MODULE=mysite.settings
redis-server --daemonize yes
celery -A mysite worker -l info & > celery_log
python3 manage.py runserver 0:8000

