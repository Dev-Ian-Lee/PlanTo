from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["owner", "title", "description", "company", "position", "due_date", "location", "salary"]