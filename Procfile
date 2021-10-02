web: gunicorn sender.wsgi:sender --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate