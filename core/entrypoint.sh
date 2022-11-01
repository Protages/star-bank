#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  python manage.py makemigrations
  python manage.py migrate
fi


exec "$@"