from django.urls import path
from login.views import LoginUser
from login.views import LogoutUser

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]