from django.urls import path
from .views import *

urlpatterns = [
    path('albums<str:pk>/', AlbumsView.as_view(), name='albums'),
    path('photo/put-like/', PutLikePhoto.as_view()),
    path('photo/delete/', DeletePhotoView.as_view()),
    path('photo/make-main/', MakeMainPhoto.as_view()),
]
