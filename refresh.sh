#!/bin/bash
DJANGO_SUPERUSER_PASSWORD=password
echo "flushing db..."
python3 manage.py flush --no-input
echo "populating db with fake records for User, MeetupGroup, Event, Tag"
python3 manage.py generateFakeRecords
echo "adding test admin"
export DJANGO_SUPERUSER_PASSWORD="password"
export DJANGO_SUPERUSER_USERNAME="admin" 
export DJANGO_SUPERUSER_EMAIL="admin@test.com"
python3 manage.py createsuperuser --noinput
