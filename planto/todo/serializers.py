from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["owner", "title", "description", "due_date", "priority", "status", "memo"]