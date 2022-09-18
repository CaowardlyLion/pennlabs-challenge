cd /opt/pennlabs-challenge
python3 bootstrap.py
gunicorn --bind 0.0.0.0:5000 wsgi:app