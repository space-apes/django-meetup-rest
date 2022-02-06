# desired url endpoints and underlying models

# REST API for social meetup type web application
- TODO: 
- TODO: prevent CSRF attacks
- TODO: describe high level features here
- TODO: update docker build instructions
- TODO: generate documentation using swagger or similar
	- check drf official docs for integrating swagger
- TODO: do all TODOs and remove all TODOS
- TODO: be satisfied with what you have and finish so you can publish this and get a job

# features 
- uses djangorestframework for REST API
- uses JWT for authentication 
- uses DRF viewsets and routes 
- includes custom User model and manager
- includes custom serializers with validators for all models accessed from API
- includes custom permissions and filters to limit access 
- includes bash refresh script to populate DB with test data /refresh.sh
- includes bash/curl script for one-off request-response cycles: /jwtTest.sh
- includes tests for all models and endpoints/permissions

### to build and run as docker container:aa
- clone git repo to local machine
- pip3 install -r requirements.txt
- create a database within your dbms for the project
- generate a new secret_key for django project
	- run django shell: python3 manage.py shell
	- from django.core.management.utils import get_random_secret_key
	- print(get_random_secret_key())
- set build-environment specific variables however you wish (i used docker-compose.yml)
	- SECRET_KEY
	- ALLOWED_HOSTS
	- DB_ENGINE
	- DB_HOST
	- DB_NAME
	- DB_USER
	- DB_PASSWORD
	- ENV_SECRET_KEY
- determine how to serve static files and python3 manage.py collectstatic
	- i served from most outward facing web server. 
- ./refresh.py
	- bash script creates migrations, populates db with fake records, adds super user
- run test server with 'python3 manage.py runserver localhost:62231'
- navigate web browser to url:port/api/token and supply credentials in JSON body
	- ADMIN
		- "username":"admin"
		- "password":"password"
	- USER
		-"username":"ftester"
		-"password":"password"
		-(can try different users by incrementing/decrementing first letter in username)


## MODELS

## END POINTS
- /api-auth/   
- /users/ 
	- {R,U,D}:	superuser
	- {C}: 		anonymous
- /users/<user_pk>/ 
	- {C,R,U,D}:	superuser
	- {R,U,D}:	user whose pk == user_pk
- /meetup_groups/ 
	- {C,R}:	superuser
	- {C,R}:	any authenticated user
	- {R}:		any user
- /meetup_groups/<meetup_group_pk>/
	- {R,U,D}:	superuser
	- {R,U,D}:	user who is admin of meetup group
	- {R}:		any user
- /meetup_groups/<meetup_group_pk>/events/ (alternate endpoint for events that filters by meetup_group)
	- {R}: any user
- /users/<user_pk>/meetup_groups/ (alternate endpoint for meetups that filters by user)
	- {R}:		superuser
	- {R}:		user whose pk == user_pk
- /events/
	- {C,R}: 	superuser
	- {C,R}:	any user that is admin of a meetup_group
	- {R}:		any user
- /events/<event_pk>/
	- {R,U,D}:	superuser
	- {R,U,D}:	user with id == event.host.id
