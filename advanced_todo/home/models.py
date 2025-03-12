from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import Users
from django.utils import timezone

# Common date fields
class AbstractDateFieldMix(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True



# Task model for Weekly Schedule
class WeeklyTask(AbstractDateFieldMix):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK,blank=True, null=True)
    date = models.DateField(blank=True, null=True)  
    time = models.TimeField(blank=True, null=True)
    task = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f"{self.day.capitalize()} - {self.time} - {self.task}"

# Task model for Start and End Day To-Do Lists
class ToDoTask(AbstractDateFieldMix):
    TASK_TYPE = [
        ('start', 'Start Day'),
        ('end', 'End Day'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=5, choices=TASK_TYPE,blank=True, null=True)
    task = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.task}"

class Note(AbstractDateFieldMix):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_checklist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChecklistItem(AbstractDateFieldMix):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="checklist_items")
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text