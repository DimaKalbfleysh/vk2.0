from .views import *
from django.urls import path

urlpatterns = [
    path('groups/', GroupsView.as_view(), name='groups'),
    path('public<str:pk>/', GroupView.as_view(), name='group'),
    path('public/create/', GroupCreateView.as_view(), name='group-create'),
    path('public<str:pk>/edit/', GroupEditView.as_view(), name='group-edit'),
    path('public<str:pk>/subscribe/', SubscribeToGroup.as_view(), name='subscribe-to-group'),
]