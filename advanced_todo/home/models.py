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
        ('parking', 'Parking Lot'),
        ('recovery', 'Recovery Task'),
    ]

    category = models.CharField(max_length=20, choices=TASK_CATEGORIES, default='inbox')
    headline = models.CharField(_('Headline'), max_length=255, blank=True, null=True, unique=True)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    is_active = models.BooleanField(_('Status'), default=True)
    is_task = models.BooleanField(_('Task'), default=True)
    created_by = models.ForeignKey(Users, related_name="task_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(Users, related_name="task_updated_by", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_category_display()}: {self.headline}"
