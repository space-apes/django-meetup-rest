from django.shortcuts import render
from api.models import User, MeetupGroup, Event, Tag
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, MeetupGroupSerializer, TagSerializer, EventSerializer

#retrieve request query parameters like so: 
#self.request.query_params.get('make')

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]


class MeetupGroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows meetup groups to be viewed or edited. 
		
	Includes queryset parameters?
	- anonymous / by current logged in user
	- by tag 
	"""

	serializer_class = MeetupGroupSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = MeetupGroup.objects.all()


class TagViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tags to be viewed or edited
	"""
	serializer_class = TagSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Tag.objects.all()
