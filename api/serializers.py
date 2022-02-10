from api.models import User, Event, Tag, MeetupGroup, Event
from rest_framework import serializers

#to capture model relationships in api responses, need to describe relationships
#in serializers too. the 'related_name' field is really important here


#TODO: deal with creating meetup groups with multiple tags associated

"""
    custom field validators like this:

    def multiple_of_ten(value):
        if value % 10 != 0:
            raise serializers.ValidationError('Not a multiple of ten')

    class GameRecord(serializers.Serializer):
        score = IntegerField(validators=[multiple_of_ten])
"""

class UserSerializer(serializers.ModelSerializer):
    meetup_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
            model = User
            fields = ['url', 'username', 'email', 'meetup_groups', 'events', 'first_name', 'last_name', 'password']
            #ensure password is changeable but not observable
            extra_kwargs = {
                'password': {'write_only': True}
            }

    # override create method to ensure passwords are hashed
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # again, added custom update method to ensure password hashing 
    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        if 'password' in validated_data.keys():
            user.set_password(validated_data['password'])
            user.save()
        return user
        
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


    #override create method to force user who created group to be admin
    def create(self, validated_data):
        meetup_group = MeetupGroup(**validated_data)
        meetup_group.admin = self.context['request'].user
        meetup_group.save()
        return meetup_group

class EventSerializer(serializers.HyperlinkedModelSerializer):
    meetup_group= serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    host = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
            model = Event
            fields = ['name', 'description', 'date', 'address', 'date_created', 'host', 'meetup_group', 'participants']

    #TODO: event serializer create forces meetup group field and host field

