from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import Users

# Common date fields
class AbstractDateFieldMix(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True

# Generic Task Model
class Task(AbstractDateFieldMix):
    TASK_CATEGORIES = [
        ('inbox', 'Inbox'),
        ('important', 'Important Task'),
        ('urgent', 'Urgent Task'),
        ('daily', 'Daily Task'),
        ('weekly', 'Weekly Task'),
        ('monthly', 'Monthly Task'),
        ('parkinglot', 'Parking Lot'),
        ('recovery', 'Recovery Task'),
    ]

    category = models.CharField(max_length=20, choices=TASK_CATEGORIES, default='inbox')
    headline = models.CharField(_('Headline'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    is_active = models.BooleanField(_('Status'), default=True)
    is_task = models.BooleanField(_('Task'), default=True)
    created_by = models.ForeignKey(Users, related_name="task_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(Users, related_name="task_updated_by", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_category_display()}: {self.headline}"
    
    class Meta : 
        verbose_name          = "Task"
        verbose_name_plural   = "Tasks"

        constraints = [
            models.UniqueConstraint(fields=['headline', 'category'], name='unique_headline_per_category')
        ]  # ✅ Added unique constraint




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
