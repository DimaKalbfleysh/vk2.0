from django.urls import path
from .views import *

urlpatterns = [
    path('', InitRegisterUser.as_view(), name='init_register'),
    path('<str:username>/', FinalRegisterUser.as_view(), name='final_register'),
    path('verify/<str:pk>/', Verify.as_view(), name='verify'),
]