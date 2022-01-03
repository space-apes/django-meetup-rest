from datetime import datetime 
from .models import User, Tag, Event, MeetupGroup

def generateFakeUsers():
	curCharCode = 97
	userNameDicts= [
		{
			"first_name": "Abalone",
			"last_name": "Birkenstocks",
		},
		{
			"first_name": "Calliope",
			"last_name": "Dungweaver",
		},
		{
			"first_name": "Eudaimonia",
			"last_name": "Fragglerock",
		},
		{
			"first_name": "Gabrielle",
			"last_name": "Hendrix",
		},
		{
			"first_name": "Impsnake",
			"last_name": "Julipjoy",
		},
		{
			"first_name": "Klaxon",
			"last_name": "Livingcheesy",
		},
		{
			"first_name": "Mungbean",
			"last_name": "Nor'Easter",
		},
		{
			"first_name": "Owlbear",
			"last_name": "Punctuality",
		}
	]

	for curName in userNameDicts:
		u = User.objects.create(
				first_name=curName['first_name'],
				last_name=curName['last_name'],
				username = f"{chr(curCharCode)}tester",
				email=f"{chr(curCharCode)}tester@test.com",
				password="password"
				)


		curCharCode+=1
	
	User.objects.get(pk=1).is_superuser = 1 

def generateFakeTags():
	tagNameList = ['singles', 'dating', 'archery', 'social', 'target practice', 'arrows', 'romance', 'machine learning', 'fletching', 'robin', 'hood', 'corporate', 'employed', 'neural networks', 'classifiers', 'regression', 'prediction', 'big data']

	for curName in tagNameList:
		Tag.objects.create(name=curName, create_date=datetime.now())

def generateFakeMeetupGroups():
	meetupGroups = [
		{
			"name" : 'North Bay ML',
			"description" : "Talk about the latest machine learning tools and technologies",
			"create_date" : datetime.now(),
			"members_list": [1,2,3],
			"tags_list": ['neural networks', 'classifiers', 'regression', 'prediction', 'big data']

		},
		{
			"name" : 'Simply Shooting',
			"description" : 'We are a group of archers of all skill levels. Join us at the range!',
			"create_date" : datetime.now(),
			"members_list": [4,5,6],
			"tags_list" : ['archery','arrows','fletching', 'robin', 'hood']

		},
		{
			"name" : 'Dating Professionals',
			"description" : 'Find your match. We host weekly social events for busy people',
			"create_date" : datetime.now(),
			"members_list": [6,7,8],
			"tags_list" : ['singles', 'dating', 'corporate', 'employed', 'social']

		},
		{
			"name" : "Cupid's Arrow",
			"description" : 'Single? Love archery? Find a romantic match with an arrow to the heart!',
			"create_date" : datetime.now(),
			"members_list": [1,2,3],
			"tags_list" : ['archery','arrows', 'singles', 'social', 'target practice']

		}

	]

	for curGroup in meetupGroups:
		m = MeetupGroup(
				name = curGroup['name'],
				description = curGroup['description'],
				create_date = curGroup['create_date'],
			       )
		m.save()
		for tagName in curGroup['tags_list']:
			m.tag_set.add(Tag.objects.get(name=tagName))
		for member_id in curGroup['members_list']:
			m.members.add(User.objects.get(pk=member_id))
		m.save()

	

def generateAll():
	generateFakeUsers()
	generateFakeTags()
	generateFakeMeetupGroups()	
