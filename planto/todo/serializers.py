from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # User의 Task 객체를 PrimaryKeyRelatedField로 연결
    tasks = serializers.PrimaryKeyRelatedField(many = True, queryset = Task.objects.all())

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "tasks"]