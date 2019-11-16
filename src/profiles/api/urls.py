from django.urls import path, include
from .views import (
    ProfileList, ProfileDetail, Profiles5List, ProfileFriendsList, RelationshipViewset, my_invations_received
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'relationship', RelationshipViewset, basename='post')


urlpatterns = [
    path("", include(router.urls)),
    path('invites/', my_invations_received, name='profile-invites'),
    path('rel/', ProfileList.as_view(), name="profile-list"),
    path('recs/', Profiles5List.as_view(), name="profile-5-list"),
    path('friends/', ProfileFriendsList.as_view(), name='profile-friends'),
    path('<pk>/', ProfileDetail.as_view(), name="profile-detail"),

]
