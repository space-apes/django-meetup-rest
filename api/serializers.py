from api.models import User, Event, Tag, MeetupGroup, Event
from rest_framework import serializers

#to capture model relationships in api responses, need to describe relationships
#in serializers too. the 'related_name' field is really important here


#TODO: validators on serializers!!!
#TODO: distinct serializers/valdation for different http methods!


class UserSerializer(serializers.HyperlinkedModelSerializer):
	meetup_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'meetup_groups', 'first_name', 'last_name']

	# if want to create new instances from serializer, had to override create method
	# to use the User.objhecs.create_user method to capture hashing
	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class TagSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tag
		fields = ['name', 'create_date']

class MeetupGroupSerializer(serializers.HyperlinkedModelSerializer):
	members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	admin = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
	tags = serializers.PrimaryKeyRelatedField(many = True, read_only=True)
	class Meta:
		model = MeetupGroup
		#do i need to include host_id if i am adding a relationship through serializers?
		#NO these are model fields not DB record fields. you are still in python land!
		fields = ['url', 'name', 'create_date', 'description', 'members', 'admin', 'tags']

class EventSerializer(serializers.HyperlinkedModelSerializer):
	meetup_group= serializers.PrimaryKeyRelatedField(many=False, read_only=True)
	host = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
	class Meta:
		model = Event
		fields = ['name', 'description', 'date', 'address', 'date_created', 'host', 'meetup_group' ]
