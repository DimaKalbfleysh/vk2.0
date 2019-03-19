from django.urls import path
from .views import *


urlpatterns = [
    path('di/', DialogsView.as_view(), name='di'),
    path('im/', MessagesView.as_view(), name='im'),
    path('up/message/', UpdateMessagesView.as_view(), name='up'),
    path('up/dialog/', UpdateDialogsView.as_view(), name='up'),
]