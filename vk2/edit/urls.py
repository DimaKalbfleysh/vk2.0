from .views import *
from django.urls import path

urlpatterns = [
    path('', EditUser.as_view(), name='edit'),

]