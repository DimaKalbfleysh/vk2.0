from .views import *
from django.urls import path

urlpatterns = [
    path('id<str:pk>/', MainView.as_view(), name='account'),
    path('friends<str:pk>/', FriendsView.as_view(), name='friends')
]