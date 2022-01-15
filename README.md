# desired url endpoints and underlying models

# REST API for social meetup type web application
- TODO: describe high level features here
- TODO: generate documentation using swagger or similar

# features 
- uses djangorestframework for REST API
- uses JWT for authentication 
- uses DRF viewsets and routes 
- includes custom user model and manager
- includes custom serializers with validators for all models accessed from API
- includes custom permissions and filters to limit access 
- includes refresh script to populate DB with test data /refresh.sh
- includes curl script for one-off request-response cycles: /jwtTest.sh

### to build and run as docker container:a
- clone git repo to local machine
- pip3 install -r requirements.txt
- create a database within your dbms for the project
- generate a new secret_key 
- set build-environment specific variables through docker
	- SECRET_KEY
	- ALLOWED_HOSTS
	- DB_ENGINE
	- DB_HOST
	- DB_NAME
	- DB_USER
	- DB_PASSWORD
	- ENV_SECRET_KEY
- determine how to serve static files and python3 manage.py collectstatic


- use bash script to create migrations, populate db with fake records, add super user
- run test server with 'python3 manage.py runserver localhost:62231'
- navigate web browser to url:port/api/token and supply credentials in JSON body
	- ADMIN
		- "username":"admin"
		- "password":"password"
	- USER
		-"username":"ftester"
		-"password":"password"
		-(can try different users by incrementing/decrementing first letter in username)

## END POINTS
- /api-auth/ 
- /admin/  
- /users/ 
	- {C,R,U,D}:	superuser
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
