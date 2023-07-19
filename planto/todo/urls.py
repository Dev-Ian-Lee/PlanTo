from django.urls import path
from .views import *

urlpatterns = [
    path('users', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
    path('register', Registration.as_view()),
    path('login', Login.as_view()),
]
