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
		IsSuperUserOrTargetUser)

#retrieve request query parameters like so: 
	#self.request.query_params.get('make')
#access slug values from urlconfs with 
	#self.kwargs.get('slugName')

#useful mixins when using viewsets.GenericViewSet:
# includes create, list, retrieve operations
# - ListModelMixin
# - CreateModelMixin
# - RetrieveModelMixin
# - UpdateModelMixin
# - DestroyModelMixin




#below is using viewsets. super clean but not sure yet how to make more specific 
#endpoints for relations/nested data

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	Only admin users should be able to see raw User data
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [IsSuperUserOrTargetUser]
		
	
class MeetupGroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows meetup groups to be viewed or edited.
	admin has all permissions
	all other users have only read permissions
	"""

	serializer_class = MeetupGroupSerializer
	permission_classes = [IsSuperUserOrReadOnly]
	queryset = MeetupGroup.objects.all()


class TagViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tags to be viewed or editeda
	all types of users should be able to see tag data
	"""
	serializer_class = TagSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Tag.objects.all()

#DONT FORGET TO ADD ISADMINORSELF PERMISSIONS
class UserMeetupGroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows meetup groups associated with a user to be 
	viewed. If user is admin, then allow update, partial update, delete
	on meetups
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

