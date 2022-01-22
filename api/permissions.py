from rest_framework import permissions

#can access slug values from view.kwargs

class IsSuperUserOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.method == 'GET' or request.user.is_superuser

class IsSuperUserOrAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.is_superuser or obj.admin == request.user

class IsSuperUserOrHost(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.is_superuser or obj.host == request.user

class IsSuperUserOrTargetUser(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.is_superuser:
			return True
		elif request.user.is_authenticated and view.action in ['retrieve','update','destroy']:
			return True
		else:
			return False

	def has_object_permissions(self,request, view, obj):
		return request.user.id == obj.id

class IsAnyUserReadOnly(permissions.BasePermission):
	meetups = "attempting non read-only action"
	def has_permission(self,request,view):
		return view.action in ['list', 'retrieve']
	
	def has_object_permission(self,request,view,obj):
		return view.action in ['list', 'retrieve']
	

class IsAuthenticatedUserCreating(permissions.BasePermission):
	message = "attempting to create when not authenticated"
	def has_permission(self,request,view):
		return True
	
	def has_object_permission(self,request,view,obj):
		return request.user.is_authenticated and view.action == 'create'


class IsAnonymousUserCreating(permissions.BasePermission):
	message = "attempting to create when not anonymous"
	def has_permission(self,request,view):
            return view.action == 'create'
	
	def has_object_permission(self,request,view,obj):
	    return request.user.is_anonymous and view.action == 'create'
	

class IsSuperUserOrAdminUpdatingOrDestroying(permissions.BasePermission):
	message= "attempting to update, partial update, or destroy a when not super user or admin"
	
	def has_permission(self,request,view):
	    return True
	

	def has_object_permission(self,request,view,obj):
            return\
                    (request.user.is_superuser or request.user == obj.admin) and\
                    view.action in ['update', 'partial_update','destroy']
