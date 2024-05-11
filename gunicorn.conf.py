# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
timeout = 120  # Increase the timeout to 120 seconds
loglevel = 'debug'