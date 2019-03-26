from django.urls import path
from .views import *

urlpatterns = [
    path('search/', Search.as_view())
]
