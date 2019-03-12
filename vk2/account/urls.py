from photo.views import AlbumsView, DeletePhotoView, MakeMainPhoto, PutLikePhoto
from message.views import DialogView, MessageView, UpdateMessagesView
from post.views import PostView, PutLikePost, DeletePostView
from group.views import GroupsView, GroupView
from .views import *
from django.urls import path

urlpatterns = [
    path('id<str:pk>/', MainView.as_view(), name='account'),
    path('albums<str:pk>/', AlbumsView.as_view(), name='albums'),
    path('friends<str:pk>/', FriendsView.as_view(), name='friends'),
    path('di/', DialogView.as_view(), name='di'),
    path('im/', MessageView.as_view(), name='im'),
    path('up/', UpdateMessagesView.as_view(), name='up'),
    path('ps/', PostView.as_view(), name='ps'),
    path('groups/', GroupsView.as_view(), name='groups'),
    path('public<str:pk>/', GroupView.as_view(), name='group'),
    path('dl/', DeletePhotoView.as_view()),
    path('mk/', MakeMainPhoto.as_view()),
    path('dlp/', DeletePostView.as_view()),
    path('lkp/', PutLikePost.as_view()),
    path('lkph/', PutLikePhoto.as_view()),
]