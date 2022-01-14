from rest_framework import permissions

#can access slug values from view.kwargs

class IsSuperUserOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.method == 'GET' or request.user.is_superuser

class IsSuperUserOrAdmin(permissions.BasePermission):
	def has_permission(self, request, view, obj):
		return request.user.is_superuser or obj.admin == request.user

class IsSuperUserOrHost(permissions.BasePermission):
	def has_permission(self, request, view, obj):
		return request.user.is_superuser or obj.host == request.user

class IsSuperUserOrTargetUser(permissions.BasePermission):
	def has_permission(self, request, view):
		if not request.user.is_authenticated:
			return False
		return (request.user.is_superuser) or (request.user.id == int(view.kwargs.get('pk')))

class IsAnyUserReadOnly(permissions.BasePermission):
	def has_permission(self,request,view):
		print(f"IsAnyUserReadOnly: {view.action in ['list', 'retrieve']})")
		return view.action in ['list', 'retrieve']


class IsAuthenticatedUserCreating(permissions.BasePermission):
	def has_permission(self,request,view):
		print(f'isAuthenticatedUserCreating:\
				{request.user.is_authenticated and view.action == "create"}')
		return request.user.is_authenticated and view.action == 'create'


class IsSuperUserOrAdminUpdatingOrDestroying(permissions.BasePermission):
	message= "attempting to update, partial update, or destroy a when not super user or admin"
	def has_permission(self,request,view):
		print(f'IsSuperUserOrAdminUpdatingOrDestroying::has_permission')
		return True
	
	def has_object_permission(self,request,view,obj):
		print(f'IsSuperUserOrAdminUpdatingOrDestroying::has_object_permission')
		return\
			(request.user.is_superuser or request.user == obj.admin) and\
			view.action in ['update', 'partial_update','destroy']
"""
class CustomMeetupPermission(permissions.BasePermission):
#	any user should be able to GET a listing or detail
#	only super users or authenticated users should be able to create new entries
#	only super users or meetup group admins should be able to update or delete entries
	def has_object_permission(self, request, view, obj):
		if request.method =='GET' and (view.action in ['list', 'retrieve']):
			return True
		elif view.action == 'create':
			return request.user.is_superuser or request.user.is_authenticated()
		elif view.action in ['update', 'partial_update', 'destroy']:
			return request.user.is_superuser or request.user == obj.admin
		else:
 		 	return False
"""


