from django.urls import path
from .views import *


urlpatterns = [
    path('feed/', NewsView.as_view(), name='feed'),
]