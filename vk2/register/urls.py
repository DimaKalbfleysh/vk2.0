from django.urls import path
from register.views import FinalRegisterUser
from register.views import InitRegisterUser
from register.views import Verify

urlpatterns = [
    path('', InitRegisterUser.as_view(), name='init_register'),
    path('<str:username>/', FinalRegisterUser.as_view(), name='final_register'),
    path('verify/<str:pk>/', Verify.as_view(), name='verify'),
]