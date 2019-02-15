from .views import *
from django.urls import path

urlpatterns = [
    path('id<str:pk>/', MainView.as_view(), name='account'),
    path('albums<str:pk>/', AlbumsView.as_view(), name='albums'),
    path('friends<str:pk>/', FriendsView.as_view(), name='friends'),
    path('di/', DialogView.as_view(), name='di'),
    path('im/', MassageView.as_view(), name='im')
]