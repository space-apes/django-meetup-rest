from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, MeetupGroupViewSet, UserMeetupGroupViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'meetup_groups', MeetupGroupViewSet)

"""
/users/
/users/1
/users/1/meetup_groups
/users/1/events
/users/me/meetup_groups
/users/me/events
/meetup_groups/
/meetup_groups/search?searchstring
/meetup_groups/1/
/meetup_groups/1/tags
/meetup_groups/1/events
/meetup_groups/1/members
/events/
/events/1/
/tags/
/tags/1/
/tags/1/meetups/
"""

urlpatterns = [
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('admin/', admin.site.urls),
	path('', include(router.urls)),
	path('users/<int:user_pk>/meetup_groups/', UserMeetupGroupViewSet.as_view({'get':'list'})),
	path('users/<int:user_pk>/meetup_groups/<int:meetup_group_pk>/', UserMeetupGroupViewSet.as_view({'get':'retrieve'})),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
