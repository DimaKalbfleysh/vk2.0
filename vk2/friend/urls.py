from .views import *
from django.urls import path

urlpatterns = [
    path('friends<str:pk>/', FriendsView.as_view(), name='friends'),
    path('friends<str:pk>/all_requests/', FriendsAllRequest.as_view()),
    path('friends<str:pk>/all_users/', FriendsAllUsers.as_view()),
    path('friendship<str:pk>/request/', Request.as_view()),
    path('friendship<str:pk>/accept/', Accept.as_view()),
    path('up/friendship/', UpdateFriendshipRequest.as_view())
]