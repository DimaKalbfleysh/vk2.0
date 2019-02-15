from django.urls import path
from register.views import FinalRegisterUser
from register.views import InitRegisterUser

urlpatterns = [
    path('', InitRegisterUser.as_view(), name='init_register'),
    path('<str:username>/', FinalRegisterUser.as_view(), name='final_register'),
]