#populate DB with some test data. adds Users, MeetupGroups, Events and records to capture relationships between them.

from django.core.management.base import BaseCommand, CommandError
import datetime
from django.utils import timezone
from api.models import User, Tag, Event, MeetupGroup
from random import randint


def randomDatetime():
	return timezone.now() + datetime.timedelta(days=randint(-10,10), hours=randint(-10, 10))

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
		},
		{
			"first_name": "Quiche",
			"last_name": "Razzleberries",
		},
		{
			"first_name": "Slipper",
			"last_name": "Traction",
		},
		{
			"first_name": "Uhura",
			"last_name": "Victorinox",
		},
		{
			"first_name": "Wakefield",
			"last_name": "Xenophobe",
		},
		{
			"first_name": "Yuffie",
			"last_name": "Zarathustra",
		},
	]

	for curName in userNameDicts:
		u = User.objects.create_user(
				first_name=curName['first_name'],
				last_name=curName['last_name'],
				username = f"{chr(curCharCode)}tester",
				email=f"{chr(curCharCode)}tester@test.com",
				password="password"
				)


		curCharCode+=1
	

def generateFakeTags():
	tagNameList = ['singles', 'dating', 'archery', 'social', 'target practice', 'arrows', 'romance', 'machine learning', 'fletching', 'robin', 'hood', 'corporate', 'employed', 'neural networks', 'classifiers', 'regression', 'prediction', 'big data']

	for curName in tagNameList:
		Tag.objects.create(name=curName, create_date=randomDatetime())

def generateFakeMeetupGroups():
	meetupGroups = [
		{
			"name" : 'North Bay ML',
			"description" : "Talk about the latest machine learning tools and technologies",
			"create_date" : randomDatetime(),
			"members_list": [1,2,3,4,5,6],
			"tags_list": ['neural networks', 'classifiers', 'regression', 'prediction', 'big data']

		},
		{
			"name" : 'Simply Shooting',
			"description" : 'We are a group of archers of all skill levels. Join us at the range!',
			"create_date" : randomDatetime(),
			"members_list": [4,6,8],
			"tags_list" : ['archery','arrows','fletching', 'robin', 'hood']

		},
		{
			"name" : 'Dating Professionals',
			"description" : 'Find your match. We host weekly social events for busy people',
			"create_date" : randomDatetime(),
			"members_list": [6,7],
			"tags_list" : ['singles', 'dating', 'corporate', 'employed', 'social']

		},
		{
			"name" : "Cupid's Arrow",
			"description" : 'Single? Love archery? Find a romantic match with an arrow to the heart!',
			"create_date" : randomDatetime(),
			"members_list": [4.,6,8,9,10,11],
			"tags_list" : ['archery','arrows', 'singles', 'social', 'target practice']

		}

	]

	for curGroup in meetupGroups:
		m = MeetupGroup(
				name = curGroup['name'],
				description = curGroup['description'],
				create_date = curGroup['create_date'],
				admin = User.objects.get(pk=curGroup['members_list'][0])
			       )
		m.save()
		for tagName in curGroup['tags_list']:
			m.tags.add(Tag.objects.get(name=tagName))
		for member_id in curGroup['members_list']:
			m.members.add(User.objects.get(pk=member_id))
		m.save()

def generateFakeEvents():
	eventDictList = [
		{
			"name": "deep belief network foundation chat!",
			"description": " meet us at the spot for a conversation about restricted boltzmann machines",
			"meetup_group_id": 1,
			"date_created": timezone.now(),
			"address": "123 west cherry street",
			"date": randomDatetime()

		},
		{
			"name": "Beginners Coffee and Hack",
			"description": "for this meeting we will go step by step through logistic regression, a very important fundamental ML tool",
			"meetup_group_id": 1,
			"date_created": timezone.now(),
			"address": "123 west cherry street",
			"date": randomDatetime()

		},
		{
			"name": "Self Organizing Maps",
			"description": "Pastries and stimulating conversation at the spot!",
			"meetup_group_id": 1,
			"date_created": timezone.now(),
			"address": "123 west cherry street",
			"date": randomDatetime()

		},
		{
			"name": "deep belief network foundations",
			"description": "understanding restricted boltzmann machines",
			"meetup_group_id": 1,
			"date_created": timezone.now(),
			"address": "123 west cherry street",
			"date": randomDatetime()

		},
		{
			"name": "Weekly Shootout!",
			"description": "Bring crossbows, composite bows, small trebuchets, all are welcome at the weekly shootout. ",
			"meetup_group_id": 2,
			"date_created": timezone.now(),
			"address": "A Street Shooting range: 221 A street, 90210",
			"date": timezone.now()+datetime.timedelta(days =7)

		},
		{
			"name": "Weekly Shootout!",
			"description": "Bring crossbows, composite bows, small trebuchets, all are welcome at the weekly shootout. ",
			"meetup_group_id": 2,
			"date_created": timezone.now(),
			"address": "A Street Shooting range: 221 A street, 90210",
			"date": timezone.now()+datetime.timedelta(days = 14)

		},
		{
			"name": "Monthly Mixer",
			"description": "Find your match at the Edison Club. Dress to impress!",
			"meetup_group_id": 3,
			"date_created": timezone.now(),
			"address": "Edison Club: 17479 E. Derision Lane, 90210",
			"date": timezone.now()

		},
		{
			"name": "Monthly Mixer",
			"description": "Find your match at the Edison Club. Dress to impress!",
			"meetup_group_id": 3,
			"date_created": timezone.now(),
			"address": "Edison Club: 17479 E. Derision Lane, 90210",
			"date": timezone.now()+datetime.timedelta(days=30)

		},
		{
			"name": "Monthly Mixer",
			"description": "Find your match at the Edison Club. Dress to impress!",
			"meetup_group_id": 3,
			"date_created": timezone.now(),
			"address": "Edison Club: 17479 E. Derision Lane, 90210",
			"date": timezone.now()+datetime.timedelta(days=60)

		},
		{
			"name": "Speed dating for busy people",
			"description": "25% success rate so far! Join us at the Tuna Club and leave the small talk at home!",
			"meetup_group_id": 3,
			"date_created": timezone.now(),
			"address": "Tuna Club: 750 Kernel Junction, 90210",
			"date": randomDatetime()

		},
		{
			"name": "A street shootout",
			"description": "Hopefully a sunny day. Bring your aim and your game!",
			"meetup_group_id": 4,
			"date_created": timezone.now(),
			"address": "A Street Shooting range: 221 A street, 90210",
			"date": timezone.now()+datetime.timedelta(days=30)

		}

	]

	for eventDict in eventDictList:
		m = MeetupGroup.objects.get(pk=eventDict['meetup_group_id'])	
		member_list = m.members.all()
		e = Event(
				name = eventDict['name'],
				description = eventDict['description'],
				address= eventDict['address'],
				date_created = eventDict['date_created'],
				date = eventDict['date'],
				meetup_group = m,
				host = m.admin)
		e.save()
		
		#make sure to add host to participants list
		#print(f"len of member list before removing admin: {len(member_list)}")
		e.participants.add(m.admin)
		member_list = member_list.exclude(id=m.admin.id)
		
		#remove one random person from meetup group and add rest as participants
		#print(f"len of member list after removing admin: {len(member_list)}")
		random_index = randint(0, len(member_list)-1)
		#print(f"random index from member_list is: {random_index}")
		random_member = member_list.all()[random_index]
		#print(f"random member is: {random_member}")
		member_list = member_list.exclude(id=random_member.id)

		for member in member_list:
			e.participants.add(member)

		e.save()


class Command(BaseCommand):
	help='run all functions to populate db with fake test cases for User, MeetupGroup, Tag, and Event models.'

	def handle(self, *args, **options):
		generateFakeUsers()
		superuser = User.objects.get(pk=1)
		superuser.is_superuser = True
		superuser.save()

		generateFakeTags()
		generateFakeMeetupGroups()
		generateFakeEvents()
		self.stdout.write(self.style.SUCCESS('successfully populated db. db explorer'))
		
