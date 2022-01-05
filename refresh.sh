#!/bin/bash
echo "flushing db..."
python3 manage.py flush --no-input
echo "populating db with fake records for User, MeetupGroup, Event, Tag"
python3 manage.py generateFakeRecords
echo "adding test admin"
python3 manage.py createsuperuser --email admin@example.com --username admin --no-input
