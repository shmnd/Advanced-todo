from django.shortcuts import render
from django.views import View
from home.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
class HomeView(LoginRequiredMixin,View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Task LIST'

    def get(self, request, *args, **kwargs):
        # Count tasks based on category
        self.context['total_inbox_tasks'] = Task.objects.filter(category='inbox', is_active=True).count()
        self.context['total_important_tasks'] = Task.objects.filter(category='important', is_active=True).count()
        self.context['total_urgent_tasks'] = Task.objects.filter(category='urgent', is_active=True).count()
        self.context['total_daily_tasks'] = Task.objects.filter(category='daily', is_active=True).count()
        self.context['total_weekly_tasks'] = Task.objects.filter(category='weekly', is_active=True).count()
        self.context['total_monthly_tasks'] = Task.objects.filter(category='monthly', is_active=True).count()
        self.context['total_parking_tasks'] = Task.objects.filter(category='parking', is_active=True).count()
        self.context['total_recovery_tasks'] = Task.objects.filter(category='recovery', is_active=True).count()

        # Total count of all active tasks
        self.context['total_tasks'] = Task.objects.filter(is_active=True).count()

        return render(request, "admin/home/dashboard.html", self.context)
