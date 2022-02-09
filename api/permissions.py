from rest_framework import permissions
from api.models import *

#can access slug values from view.kwargs

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::IsSuperuser VIEW? {request.user.is_superuser}")
        return request.user.is_superuser

class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::isAnonymous user VIEW? {request.user.is_anonymous}")
        return request.user.is_anonymous

class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::isAuthenticated user VIEW? {request.user.is_authenticated}")
        return request.user.is_authenticated

class IsTargetedUser(permissions.BasePermission):
    message="attempting to access user resource that does not belong to you"
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not 'pk' in view.kwargs.keys():
            return False
        
        return request.user.id == int(view.kwargs['pk'])

class IsRequestingGet(permissions.BasePermission):
    message="is not requesting GET"
    def has_permission(self, request, view):
        print(f"permissions: isRequestingGet? {request.method=='GET'}")
        return request.method == 'GET'

class IsRequestingPost(permissions.BasePermission):
    message="is not requesting POST"
    def has_permission(self, request, view):
        print(f"permissions: isRequestingPost? {request.method=='POST'}")

        return request.method == 'POST'

class IsTheMeetupGroupAdmin(permissions.BasePermission):
    message="attempting to modify meetup group you are not admin of"
    def has_permission(self, request, view):
            print(f"permissions: isTheMeetupGroupAdmin VIEW? False")
            return True

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, MeetupGroup):
            print(f"permissions: isMeetupGroupAdmin OBJ? not an instance of MeetupGroup!")
            return False
        print(f"permissions: isTheMeetupGroupAdmin obj? {request.user == obj.admin}")
        return request.user == obj.admin

class IsTheEventHost(permissions.BasePermission):
    message="attempting to modify event you are not host of"
    def has_permission(self, request, view):
        return False

    def has_object_permission(self,request,view,obj):
        if not isinstance(obj, MeetupGroup):
            return False
        return request.user == obj.host

class IsMemberOfMeetupGroupAssociatedWithEvent(permissions.BasePermission):
    message="attempting to retrieve event of meetup group you are not a member of"
    def has_permission(self,request,view):
        return False

    def has_object_permission(self,request,view,obj):
        if not isinstance(obj, Event):
            return False

        return request.user in obj.members.all()

    
class IsSuperUserOrAdminUpdatingOrDestroying(permissions.BasePermission):
    message= "attempting to update, partial update, or destroy a when not super user or admin"
    
    def has_permission(self,request,view):
        return False
    

    def has_object_permission(self,request,view,obj):
        return\
                (request.user.is_superuser or request.user == obj.admin) and\
                view.action in ['update', 'partial_update','destroy']
