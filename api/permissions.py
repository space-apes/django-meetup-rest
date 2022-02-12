from rest_framework import permissions
from api.models import *

#can access slug values from view.kwargs

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::IsSuperuser view? {request.user.is_superuser}")
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        print(f"permissions::IsSuperuser obj? {request.user.is_superuser}")
        return request.user.is_superuser

class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::isAnonymous user view? {request.user.is_anonymous}")
        return request.user.is_anonymous

    def has_object_permission(self, request, view, obj):
        print(f"permissions::isAnonymous user obj? {request.user.is_anonymous}")
        return request.user.is_anonymous

class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"permissions::isAuthenticated user VIEW? {request.user.is_authenticated}")
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print(f"permissions::isAuthenticated user obj? {request.user.is_authenticated}")
        return request.user.is_authenticated

class IsTargetedUser(permissions.BasePermission):
    message="attempting to access user resource that does not belong to you"
    """ 
    def has_permission(self, request, view):
        if 'pk' not in view.kwargs:
            print(f"permissions:: IsTargetUser view: no 'pk' so False")
            return False
        print(f"permissions:: IsTargetUser view: {request.user.id == int(view.kwargs['pk'])}, request.user.id: {request.user.id}, view.kwargs['pk']: {view.kwargs['pk']}")
        
        return request.user.id == int(view.kwargs['pk'])
     """

    def has_object_permission(self, request, view, obj):
        print(f"permissions:: IsTargetUser obj: {isinstance(obj, User) and request.user == obj}")
        return isinstance(obj, User) and request.user == obj


class IsTheMeetupGroupAdmin(permissions.BasePermission):
    message="attempting to modify meetup group you are not admin of"
    
    """
    def has_permission(self,request,view):
        perm = True
        print(f"permissions:IsTheMeetupGroupAdmin view = {perm}")
        return perm
    """
    def has_object_permission(self,request,view,obj):
        print(f"permissions:IsTheMeetupGroupAdmin? object: {request.user == obj.admin}")
        return request.user == obj.admin

class IsAMeetupGroupMember(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        print(f"permissions:IsAMeetupGroupMember? object: {request.user in obj.members}")
        return request.user == request.user in obj.members.all()

    

class IsTheEventHost(permissions.BasePermission):
    message="attempting to modify event you are not host of"

    def has_object_permission(self,request,view,obj):
        print(f"permissions:IsTheEventHost? obj: {isinstance(obj, MeetupGroup) and request.user == obj.host}")
        return request.user == obj.host

class IsMemberOfMeetupGroupAssociatedWithEvent(permissions.BasePermission):
    message="attempting to retrieve event of meetup group you are not a member of"
    
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
