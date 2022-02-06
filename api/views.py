from api.models import User, MeetupGroup, Event, Tag
from .serializers import UserSerializer, MeetupGroupSerializer, TagSerializer, EventSerializer
from rest_framework import viewsets, permissions, mixins, generics, filters, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
import re
from api.exceptions import BadSearchQueryParameterException
from api.permissions import (
                    IsSuperUser,
                    IsAnonymousUser,
                    IsAuthenticatedUser,
                    IsTargetedUser,
                    IsRequestingGet,
                    IsRequestingPost,
                    IsTheMeetupGroupAdmin,
                    IsTheEventHost,
                    IsMemberOfMeetupGroupAssociatedWithEvent,




		)

#retrieve request query parameters like so: 
	#self.request.query_params.get('make')
#access slug values from urlconfs with 
	#self.kwargs.get('slugName')


def index(request):
    pageName = request.user.username if request.user.is_authenticated else 'anonymous'
    context = {'pageName': pageName}
    return render(request, 'api/index.html', context=context)


#for explanation on permission classes, see api/permissions.py
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be CRUD'd
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser|IsTargetedUser|(IsAnonymousUser&IsRequestingPost)]


class MeetupGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MeetupGroups to be CRUD'd

    also query parameter search functionality. 
            list meetups that do case insensitive match on any search terms against meetup names or meetups with tags that have matching names
    """

    serializer_class = MeetupGroupSerializer
    permission_classes = [IsRequestingGet|IsSuperUser|IsTheMeetupGroupAdmin|(IsAuthenticatedUser&IsRequestingPost)]
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
                    
class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be CRUD'd
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be CRUD'd
    """
    serializer_class = EventSerializer
    permission_classes = [IsSuperUser|IsTheEventHost|(IsMemberOfMeetupGroupAssociatedWithEvent&IsRequestingGet)]
    queryset = Event.objects.all()

class UserMeetupGroupViewSet(viewsets.ModelViewSet):
    """
    Alternative API endpoint to meetupgroups 
    that allows meetup groups associated with a user to be only viewed. 
    Filtered by meetup groups that user is a 'member' of 
    """
    serializer_class = MeetupGroupSerializer
    permission_classes = [IsRequestingGet|IsSuperUser|IsTheMeetupGroupAdmin|(IsAuthenticatedUser&IsRequestingPost)]
    #permission_classes = [IsSuperUserOrReadOnly]
    
    def get_queryset(self, **kwargs):
            """
            all views in this class should 
            reference only meetupgroups that are associated with the current user
            """
            user = self.request.user
            #user = get_object_or_404(User, id=self.kwargs.get('user_pk'))
            #meetup_queryset = user.meetup_groups.all()
            meetup_queryset = get_list_or_404(MeetupGroup, admin=user)
            if meetup_queryset:
                    print("HOORAY I FOUND A FILTERED QUERYSET!")
            """
            if meetup_queryset:
                    return meetup_queryset
            else:
                    raise Http404("this user is not associated with any groups")
            """

