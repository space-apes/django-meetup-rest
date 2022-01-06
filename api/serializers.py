from api.models import User, Event, Tag, MeetupGroup, Event
from rest_framework import serializers

#to capture model relationships in api responses, need to describe relationships
#in serializers too. the 'related_name' field is really important here

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups', 'first_name', 'last_name']

class TagSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tag
		fields = ['name', 'create_date']

class MeetupGroupSerializer(serializers.HyperlinkedModelSerializer):
	members = UserSerializer(many=True, read_only=True)
	admin = UserSerializer(many = False, read_only=True)
	tags = TagSerializer(many = True, read_only=True)
	class Meta:
		model = MeetupGroup
		#do i need to include host_id if i am adding a relationship through serializers?
		#NO these are model fields not DB record fields. you are still in python land
		fields = ['url', 'name', 'create_date', 'description', 'members', 'admin', 'tags']



class EventSerializer(serializers.HyperlinkedModelSerializer):
	meetup_group= MeetupGroupSerializer(many=False, read_only=True)
	class Meta:
		model = Event
		fields = ['name', 'description', 'date', 'address', 'create_date', 'host_id', 'meetup_group_id' ]
