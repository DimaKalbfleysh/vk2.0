from django.urls import path
from .views import *

urlpatterns = [
    path('post/put-like/', PutLikePost.as_view()),
    path('post/delete/', DeletePostView.as_view()),
    path('post/create/', PostView.as_view()),
    path('post/pin/', PinPostView.as_view()),
]