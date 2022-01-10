Request ->
	view ->
		serializer ->
			Model 
Model ->
	serializer -> 
		view -> 
			Response
	
TODO: generate documentation

for me, the best way to start building an API is to begin by describing 
# desired url endpoints and underlying models

# REST API for social meetup type web application
- TODO: HIGH LEVEL FEATURES

# features 
- uses djangorestframework for REST API
- uses JWT for authentication 
- uses DRF viewsets and routes 
- includes custom user model and manager
- includes custom serializers with validators for all models accessed from API
- includes custom permissions and filters to limit access 
- includes refresh script to populate DB with test data
- includes curl script for one-off request-response cycles

### TO RUN:
- install django
- hook up to db through mysite.settings.py
- use bash script to create migrations, populate db with fake records, add super user
- run test server with 'python3 manage.py runserver localhost:62231'
- navigate web browser to url:port/api/token and supply credentials in JSON body
	- ADMIN
		- "username":"admin"
		- "password":"password"
	- USER
		-"username":"ftester"
		-"password":"password"

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
