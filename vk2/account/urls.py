from .views import *
from django.urls import path

urlpatterns = [
    path('', MainPage.as_view()),
    path('id<str:pk>/', MainView.as_view(), name='account')
]