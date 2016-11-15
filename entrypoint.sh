#!/bin/bash
echo "Waiting for Postgres"
chmod 0777 scripts/wait-for-it.sh
bash scripts/wait-for-it.sh -h postgres -p 5432

echo "Installing requirements"
pip install -r requirements.txt

if [ ! -f .init ]; then
    # If you need to run a deploy script, you can do it here
    touch .init
fi

if [ "$DEVELOPMENT" ]; then
  export PYTHONUNBUFFERED=1
  echo "Starting development server"
  exec python manage.py runserver 0.0.0.0:5000 --settings={{project}}.dev
elif [ "$PRODUCTION" ]; then
  unset PYTHONUNBUFFERED
  echo "Collecting static files"
  python manage.py collectstatic --noinput
  echo "Starting production server"
  exec gunicorn --workers 3 --bind 0.0.0.0:5000 --pid /app/docker/etc/gunicorn.pid {{project}}.wsgi:application
else
  echo "No server specified, Starting /sbin/init"
  exec /sbin/init
fi
