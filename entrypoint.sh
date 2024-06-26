#!/bin/sh
python manage.py migrate

if [ "$ENV" = "development" ]; then
  python manage.py createsuperuser --noinput
  python manage.py loaddata devices/fixtures/*
fi

exec "$@"
