from rest_framework import permissions
from api.models import *

#can access slug values from view.kwargs

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsTargetedUser(permissions.BasePermission):
    message="attempting to access user resource that does not belong to you"
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request,view, obj):
        if not isinstance(obj, User):
            return False

        return request.user == obj


class IsRequestingGet(permissions.BasePermission):
    message="is not requesting GET"
    def has_permission(self, request, view):
        return request.method == 'GET'

class IsRequestingPost(permissions.BasePermission):
    message="is not requesting POST"
    def has_permission(self, request, view):
        return request.method == 'POST'

class IsTheMeetupGroupAdmin(permissions.BasePermission):
    message="attempting to modify meetup group you are not admin of"
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, MeetupGroup):
            return False
        return request.user == obj.admin

class IsTheEventHost(permissions.BasePermission):
    message="attempting to modify event you are not host of"
    def has_permission(self, request, view):
        return True

    def has_object_permission(self,request,view,obj):
        if not isinstance(obj, MeetupGroup):
            return False
        return request.user == obj.host

class IsMemberOfMeetupGroupAssociatedWithEvent(permissions.BasePermission):
    message="attempting to retrieve event of meetup group you are not a member of"
    def has_permission(self,request,view):
        return True

    def has_object_permission(self,request,view,obj):
        if not isinstance(obj, Event):
            return False

        return request.user in obj.members.all()

    
class IsSuperUserOrAdminUpdatingOrDestroying(permissions.BasePermission):
    message= "attempting to update, partial update, or destroy a when not super user or admin"
    
    def has_permission(self,request,view):
        return True
    

    def has_object_permission(self,request,view,obj):
        return\
                (request.user.is_superuser or request.user == obj.admin) and\
                view.action in ['update', 'partial_update','destroy']
