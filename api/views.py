from django.shortcuts import render
from api.models import User
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

