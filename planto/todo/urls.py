from django.urls import path
from .views import *

urlpatterns = [
    path('users', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
]
