#!/bin/bash

echo "flushing db..."
python3 manage.py flush --no-input
echo "adding new migrations if any"
python3 manage.py makemigrations
python3 manage.py migrate
echo "populating db with fake records for User, MeetupGroup, Event, Tag"
python3 manage.py generateFakeRecords
echo "adding test admin"
export DJANGO_SUPERUSER_PASSWORD="password"
export DJANGO_SUPERUSER_USERNAME="root" 
export DJANGO_SUPERUSER_EMAIL="root@test.com"
python3 manage.py createsuperuser --noinput
