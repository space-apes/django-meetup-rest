from api.models import User, MeetupGroup, Event, Tag
from .serializers import UserSerializer, MeetupGroupSerializer, TagSerializer, EventSerializer
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from api.permissions import (
		IsSuperUserOrReadOnly, 
		IsSuperUserOrAdmin, 
		IsSuperUserOrHost,
		IsSuperUserOrTargetUser,
		CustomMeetupPermission
		)

#retrieve request query parameters like so: 
	#self.request.query_params.get('make')
#access slug values from urlconfs with 
	#self.kwargs.get('slugName')


#for explanation on permission classes, see api/permissions.py
class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Users to be CRUD'd
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [IsSuperUserOrTargetUser]

class MeetupGroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows MeetupGroups to be CRUD'd
	"""

	serializer_class = MeetupGroupSerializer
	permission_classes = [CustomMeetupPermission]
	queryset = MeetupGroup.objects.all()

	#create method should set admin field to current user. 
	#TODO: Created groups should have valid tags. 

	def create(self, request, *args, **kwargs):
		serializer = MeetupGroupSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save(admin=request.user)
			return Response(serializer.data)
		return Response(serializer.errors)

class TagViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tags to be CRUD'd
	"""
	serializer_class = TagSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Tag.objects.all()

#DONT FORGET TO ADD ISADMINORSELF PERMISSIONS
class UserMeetupGroupViewSet(viewsets.ModelViewSet):
	"""
	Alternative API endpoint to meetupgroups 
	that allows meetup groups associated with a user to be only viewed. 
	Filtered by meetup groups that user is a 'member' of 
	"""
	serializer_class = MeetupGroupSerializer
	permission_classes = [IsSuperUserOrTargetUser]
	def get_queryset(self, **kwargs):
		"""
		all views in this class should 
		reference only meetupgroups that are associated with the current user
		"""
		user = get_object_or_404(User, id=self.kwargs.get('user_pk'))
		meetup_queryset = user.meetup_groups.all()
		if meetup_queryset:
			return meetup_queryset
		else:
		 	raise Http404("this user is not associated with any groups")

	@action(detail=False, methods=['get'])
	def list(self, request, *args, **kwargs):
		meetups_from_user = self.get_queryset()
		return Response(self.get_serializer(meetups_from_user, many=True).data)

	@action(detail=True, methods=['get'])
	def detail(self, request, *args, **kwargs):
		meetups_from_user = self.get_queryset()
		specified_meetup = get_object_or_404(MeetupGroup, id=self.kwargs.get('user_pk'))
		return Response(self.get_serializer(specified_meetup))

