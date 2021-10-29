release: sudo apt install wkhtmltopdf; python manage.py migrate; python manage.py load
web: gunicorn reservations.wsgi --log-file -