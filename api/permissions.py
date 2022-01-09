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
		return request.user.id == view.kwargs.get('user_pk')
