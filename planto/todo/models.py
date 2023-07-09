from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    class statusType(models.TextChoices):
        INCOMPLETE = "incomplete", "미진행"
        ONOGOING = "ongoing", "진행 중"        
        COMPLETE = "complete", "완료"

    title = models.CharField(max_length = 255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.CharField(choices = statusType.choices, max_length = 32)
    memo = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task"

class Tag(models.Model):
    task_set = models.ManyToManyField(to = "Task", through = "TaskTagRelation")
    name = models.CharField(max_length = 255)

    class Meta:
        db_table = "tag"

class TaskTagRelation(models.Model):
    task = models.ForeignKey(to = "Task", null = False, on_delete = models.CASCADE)
    tag = models.ForeignKey(to = "Tag", null = False, on_delete = models.CASCADE)

    class Meta:
        db_table = "task_tag_relation"

class Alarm(models.Model):
    task = models.ForeignKey(to = "Task", null = False, on_delete = models.CASCADE)
    alarm_datetime = models.DateTimeField()

    class Meta:
        db_table = "alarm"