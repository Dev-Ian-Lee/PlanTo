from django.urls import path
from .views import *

urlpatterns = [
    path('', JobList.as_view()),
]
