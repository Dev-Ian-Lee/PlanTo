from django.db import models
from django.conf import settings

class Job(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "jobs", on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 255)
    description = models.TextField(null = True)
    company = models.CharField(max_length = 255)
    position = models.CharField(max_length = 255)
    due_date = models.DateField()
    location = models.CharField(max_length = 255, null = True)
    salary = models.CharField(max_length = 255, null = True)
    
    class Meta:
        db_table = "job"