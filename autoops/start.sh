uwsgi --http :8006 --module autoops.wsgi:application --daemonize=/var/log/autoops.log --enable-threads --threads 6 --processes 6

python manage.py celery worker --loglevel=info 1>>/var/log/celery.log 2>>/var/log/celery_error.log &

