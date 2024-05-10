#!/bin/bash

python manage.py migrate --no-input

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi

python manage.py runserver 0.0.0.0:8000