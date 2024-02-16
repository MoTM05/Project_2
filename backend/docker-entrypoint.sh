#!/bin/bash

# Apply migrations on every startup
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput

# Run server
# Exec is needed for gunicorn process to properly receive SIGTERM and SIGKILL
exec python3 -m gunicorn core.wsgi --bind "0.0.0.0:8000" --workers=4
