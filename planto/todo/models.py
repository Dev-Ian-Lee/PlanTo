from django.db import models
from django.utils import timezone
from django.conf import settings

class Task(models.Model):
    class StatusType(models.TextChoices):
        INCOMPLETE = "incomplete", "미진행"
        ONGOING = "ongoing", "진행 중"        
        COMPLETE = "complete", "완료"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "tasks", on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 255)
    description = models.TextField(null = True, blank = True)
    due_date = models.DateField(default = timezone.now().date())
    priority = models.IntegerField(null = True, blank = True)
    status = models.CharField(choices = StatusType.choices, max_length = 32, null = True, blank = True)
    memo = models.CharField(max_length = 255, null = True, blank = True)
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