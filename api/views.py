from api.models import User, MeetupGroup, Event, Tag
from .serializers import UserSerializer, MeetupGroupSerializer, TagSerializer, EventSerializer
from rest_framework import viewsets, permissions, mixins, generics, filters, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
import re
from api.exceptions import BadSearchQueryParameterException
from api.permissions import (
		IsSuperUserOrReadOnly, 
		IsSuperUserOrAdmin, 
		IsSuperUserOrHost,
		IsSuperUserOrTargetUser,
		IsAnyUserReadOnly,
		IsAuthenticatedUserCreating,
		IsSuperUserOrAdminUpdatingOrDestroying
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

	also query parameter search functionality. 
		list meetups that do case insensitive match on any search terms against meetup names or meetups with tags that have matching names
	"""

	serializer_class = MeetupGroupSerializer
	permission_classes = [IsAnyUserReadOnly|IsAuthenticatedUserCreating|IsSuperUserOrAdminUpdatingOrDestroying]
	queryset = MeetupGroup.objects.all()
	def get_queryset(self):
		"""
			if no queryset parameter 'search' is set
				include all MeetupGroups unless a 'search' query parameter is set
			else 
				validate query parameter 'search'
				include meetup groups w names that match search terms
				and include meetup groups with tags that match search terms
		"""
		searchString = self.request.query_params.get('search')
		if not searchString:
			return self.queryset
		else:
		 	#basic validation on query parameter 'search'
			if re.search(r"[^\w\|]", searchString):
				print(f"views::meetupgroup::get_queryset: searchString is {searchString}")
				raise BadSearchQueryParameterException
		
			meetups_matching = MeetupGroup.objects\
					   .prefetch_related('tags')\
					   .filter(Q(name__iregex=searchString) | Q(tags__name__iregex=searchString))\
					   .distinct()	
			
			return meetups_matching
			

	def get_object(self):
		m = get_object_or_404(MeetupGroup, pk=self.kwargs['pk'])
		self.check_object_permissions(self.request, m)
		return m

	#create method should set admin field to current user. 
	#TODO: Created groups should have valid tags. 

	def create(self, request, *args, **kwargs):
		serializer = MeetupGroupSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save(admin=request.user)
			return Response(serializer.data)
		return Response(serializer.errors)
	
	def partial_update(self,request,*args,**kwargs):
		print(f"views::meetupgroups::partial_update: getting called!")
		kwargs['partial'] = False
		instance = self.get_object()
		self.check_object_permissions(instance, request)
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		if serializer.is_valid(raise_exception=True):
			self.perform_update(serializer)
			return Response(serializer.data)
		return Response(serializer.errors)


class TagViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tags to be CRUD'd
	"""
	serializer_class = TagSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Tag.objects.all()

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

