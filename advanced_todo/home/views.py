import json
import csv
from django.utils.timezone import now,localdate,make_aware,localtime
from django.shortcuts import get_object_or_404, render, get_object_or_404,redirect
from django.views import View
from home.models import WeeklyTask, Note, ChecklistItem,Reminder
from authentication.models import Users 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_time
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime,parse_date
from django.db import models
from django.db.models import Q 
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone

# Start Day View
class StartDayView(LoginRequiredMixin, View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Start Day'

    def get(self, request, *args, **kwargs):
        try:
            # Fetch weekly tasks and to-do tasks
            weekly_tasks = WeeklyTask.objects.filter(user=request.user).values()

            # Pass tasks to context
            self.context['weekly_tasks'] = list(weekly_tasks)

            # Render the template with context
            return render(request, "admin/home/start-day.html", self.context)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# API: Get Tasks
@method_decorator(csrf_exempt, name='dispatch')
class GetTasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            monday_str = request.GET.get('monday')

            if monday_str:
                monday = parse_date(monday_str)
                if monday:
                    saturday = monday + timedelta(days=5)
                    weekly_tasks = WeeklyTask.objects.filter(user=user, date__range=(monday, saturday))
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid Monday date'}, status=400)
            else:
                weekly_tasks = WeeklyTask.objects.filter(user=user)

            weekly_tasks_list = [
                {**model_to_dict(task), 'time': task.time.strftime('%H:%M')}
                for task in weekly_tasks
            ]
            
            return JsonResponse({
                'weekly_tasks': weekly_tasks_list,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# API: Add Task
@method_decorator(csrf_exempt, name='dispatch')
class AddTaskView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user

            # Check task type
            if data['type'] == 'weekly':
                task = WeeklyTask.objects.create(
                    user=user,
                    day=data['day'],
                    time=parse_time(data['time']),
                    task=data['task']
                )
            # Return JSON response with task ID
            return JsonResponse({'status': 'success', 'task_id': task.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



# API: Delete Task
@method_decorator(csrf_exempt, name='dispatch')
class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id, *args, **kwargs):
        try:
            task_type = request.GET.get('type')
            if task_type == 'weekly':
                task = get_object_or_404(WeeklyTask, id=task_id, user=request.user)

                if task.date < localdate():
                    return JsonResponse({'status': 'error', 'message': 'Cannot delete past tasks'}, status=403)
                
                task.delete()
            return JsonResponse({'status': 'deleted'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# API: Update Task
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            task_type = request.GET.get('type')
            
            if task_type == 'weekly':
                task = get_object_or_404(WeeklyTask, id=task_id, user=request.user)

                if task.date != localdate():
                    return JsonResponse({'status': 'error', 'message': 'Cannot edit past tasks'}, status=403)

                task.task = data['task']
                task.save()
            return JsonResponse({'status': 'updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

# ---------------------------------------------------------------- Notes -----------------------------------------------------------------------------


@login_required
def note_page(request):
    """Render the Notes Page (cards.html)"""
    return render(request, 'admin/home/cards.html')

 
@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class NoteListView(View):
    """Handles fetching and creating notes"""

    def get(self, request):
        notes = Note.objects.filter(models.Q(user=request.user) | models.Q(assigned_to=request.user)).order_by('-is_pinned', 'order')
        notes_list = []

        for note in notes:
            reminder = Reminder.objects.filter(note=note, user=request.user).first()
            reminder_time = reminder.reminder_time.strftime('%Y-%m-%dT%H:%M') if reminder else None
            repeat = reminder.repeat if reminder else "none"

            notes_list.append({
                "id": note.id,
                "title": note.title,
                "description": note.description,
                "is_pinned": note.is_pinned,
                "is_checklist": note.is_checklist,
                "reminder_time": reminder_time,
                "repeat": repeat
            })

        return JsonResponse(notes_list, safe=False)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            note = Note.objects.create(
                user=request.user,
                title=data.get('title', ''),
                description=data.get('description', ''),
                is_checklist=data.get('is_checklist', False)
            )
            return JsonResponse({'id': note.id, 'status': 'created'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class NoteDetailView(View):
    """Handles updating and deleting notes"""

    def put(self, request, note_id):
        try:
            data = json.loads(request.body)
            note = get_object_or_404(Note, id=note_id, user=request.user)
            note.title = data.get('title', note.title)
            note.description = data.get('description', note.description)
            note.save()
            return JsonResponse({'status': 'updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    def delete(self, request, note_id):
        try:
            note = get_object_or_404(Note, id=note_id)
            if note.user == request.user or note.assigned_to == request.user:
                note.delete()
                return JsonResponse({'status': 'deleted'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this note.'}, status=403)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@method_decorator(csrf_exempt, name='dispatch')
class ChecklistItemView(View):
    """Handles adding checklist items"""

    def get(self, request, note_id):
        """Fetch checklist items for a given note"""
        note = get_object_or_404(Note, id=note_id, user=request.user)
        items = note.checklist_items.values()
        return JsonResponse(list(items), safe=False)

    def post(self, request, note_id):
        try:
            data = json.loads(request.body)
            note = get_object_or_404(Note, id=note_id, user=request.user)
            item = ChecklistItem.objects.create(
                note=note,
                text=data.get('text', ''),
                is_completed=data.get('is_completed', False)
            )
            return JsonResponse({'id': item.id, 'status': 'created'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        

    def put(self, request, note_id, item_id):
        try:
            data = json.loads(request.body)
            item = get_object_or_404(ChecklistItem, id=item_id, note__user=request.user)
            item.text = data.get('text', item.text)
            item.is_completed = data.get('is_completed', item.is_completed)
            item.save()
            return JsonResponse({'status': 'updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
    def delete(self, request, note_id, item_id):
        try:
            item = get_object_or_404(ChecklistItem, id=item_id, note__user=request.user)
            item.delete()
            return JsonResponse({'status': 'deleted'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        


# /////////////////////////////////////////////////////// PIN AND DRAG //////////////////////////////////////////////////////////////// 
    
@login_required
@csrf_exempt  # Allow AJAX requests
@require_POST  # Only allow POST requests
def toggle_pin(request, note_id):
    try:
        note = get_object_or_404(Note, id=note_id)
        if note.user == request.user or note.assigned_to == request.user:
            # Toggle pin status
            note.is_pinned = not note.is_pinned
            note.save()
            return JsonResponse({'status': 'success', 'is_pinned': note.is_pinned})
        else:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this note.'}, status=403)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@csrf_exempt
@require_POST
def update_order(request):
    """Updates the order of non-pinned notes"""
    try:
        data = json.loads(request.body)
        for item in data:
            note = get_object_or_404(Note, id=item["id"], user=request.user)
            if not note.is_pinned:  # ✅ Only update order for non-pinned notes
                note.order = item["order"]
                note.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    

# /////////////////////////////////////////////////// REMINDER ////////////////////////////////////////////////////

@csrf_exempt
@login_required
def get_reminder(request, note_id):
    """Fetch reminder for a specific note"""
    try:
        reminder = Reminder.objects.filter(note_id=note_id, user=request.user).first()

        if not reminder:
            return JsonResponse({"reminder_time": "", "repeat": "none"}, status=200)  
        
        reminder_time_ist = localtime(reminder.reminder_time)
        
        return JsonResponse({
            "reminder_time": reminder_time_ist.strftime('%Y-%m-%dT%H:%M'),
            "repeat": reminder.repeat
        }, status=200)
    

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required
@csrf_exempt
def set_reminder(request, note_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reminder_time_str = data.get("reminder_time")
            repeat = data.get("repeat")

            if not reminder_time_str:
                return JsonResponse({"message": "Reminder time is required", "status": "error"}, status=400)

            note = Note.objects.get(id=note_id)
            if note.user == request.user or note.assigned_to == request.user:
                # ✅ Convert the string to a datetime object
                reminder_time = parse_datetime(reminder_time_str)
                if reminder_time is None:
                    return JsonResponse({"message": "Invalid datetime format", "status": "error"}, status=400)

                # ✅ Ensure the datetime is timezone-aware
                reminder_time = make_aware(reminder_time)

                # ✅ Create or update the reminder for this note
                reminder, created = Reminder.objects.update_or_create(
                    note=note,
                    user=request.user,
                    defaults={"reminder_time": reminder_time, "repeat": repeat}
                )

                return JsonResponse({
                    "message": "Reminder set successfully!",
                    "status": "success",
                    "reminder_time": reminder.reminder_time.strftime('%Y-%m-%dT%H:%M'),
                    "repeat": reminder.repeat
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this note.'}, status=403)
        except Note.DoesNotExist:
            return JsonResponse({"message": "Note not found", "status": "error"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error"}, status=500)



@login_required
def check_reminders(request):
    """API to check reminders and send alerts if needed."""
    
    current_time = localtime(now())  # ✅ Convert UTC to local timezone

    reminders = Reminder.objects.filter(reminder_time__lte=current_time, user=request.user)

    reminder_list = []
    for reminder in reminders:
        # print(f"Checking reminder: {reminder.reminder_time} (DB) vs {current_time} (Now)")

        reminder_list.append({
            "id": reminder.id,
            "title": reminder.note.title,
            "description": reminder.note.description,
            "repeat": reminder.repeat
        })

        # ✅ Handle Recurring Reminders
        if reminder.repeat != "none":
            next_reminder = reminder.get_next_reminder()
            if next_reminder:
                reminder.reminder_time = next_reminder
                reminder.save()
        else:
            reminder.delete()  # Remove one-time reminders

    return JsonResponse({"reminders": reminder_list})

    


@login_required
def reminder_page(request):
    categorized_reminders = {
        "Assigned": Note.objects.filter(assigned_to=request.user).distinct(),
        "Daily": Note.objects.filter(user=request.user, reminder__repeat="daily").distinct(),
        "Weekly": Note.objects.filter(user=request.user, reminder__repeat="weekly").distinct(),
        "Monthly": Note.objects.filter(user=request.user, reminder__repeat="monthly").distinct(),
        "Yearly": Note.objects.filter(user=request.user, reminder__repeat="yearly").distinct(),
    }

    return render(request, 'admin/home/reminder.html', {'reminder_notes': categorized_reminders})



@login_required
@csrf_exempt
def remove_reminders(request, reminder_id): 
    if request.method == "DELETE":
        try:
            
            reminder = Reminder.objects.filter(id=reminder_id, user=request.user).first()
            if not reminder:
                
                return JsonResponse({"message": "Reminder not found", "status": "error"}, status=404)

            reminder.delete()

            return JsonResponse({"message": "Reminder deleted successfully!", "status": "success"})
        
        except Exception as e:

            return JsonResponse({"message": str(e), "status": "error"}, status=500)

    return JsonResponse({"message": "Invalid request method", "status": "error"}, status=405)




# ---------------------------------------------------- admin -------------------------------------------

@login_required
def admin_dashboard(request):
    if not (request.user.is_staff or request.user.is_verified):
        messages.error(request, "Unauthorized User")
        return redirect('home:startday')
    
    # users = Users.objects.filter(is_staff=False).exclude(id=request.user.id) #except that user
    users = Users.objects.filter(is_staff=False).exclude(is_staff=True) #except admins
    # users = Users.objects.all()  # everyone

    user_data = []  

    for user in users:
        user_tasks = Note.objects.filter(assigned_to=user)  # ✅ Fetch tasks for each user
        user_data.append({
            "user": user,
            "tasks": user_tasks,
        })

    return render(request, "admin/home/dashboard.html", { "user_data": user_data})


@login_required
def assign_task(request):
    if request.method == "POST" and request.user.is_staff or request.user.is_verified:
        user_id = request.POST.get("user_id")
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")

        user = get_object_or_404(Users, id=user_id)
        task = Note.objects.create(
            user=request.user,  # The admin assigning the task
            assigned_to=user,   # The user receiving the task
            title=title,
            description=description,
            due_date=due_date,
        )

        return JsonResponse({"message": "Task assigned successfully", "task_id": task.id})

    return JsonResponse({"message": "Invalid request"}, status=400)



@login_required
@csrf_exempt
def delete_task(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            task = Note.objects.get(id=task_id)
            if task.user_id == request.user.id or request.user.is_staff:
                task.delete()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "error": "You do not have permission to delete this task."})
        except Note.DoesNotExist:
            return JsonResponse({"success": False, "error": "Note not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


# --------------------- export csv weekly task ----------------------------------

@login_required
def export_weekly_tasks(request, user_id):

    if not request.user.is_staff:
        return redirect('home:startday')

    user = get_object_or_404(Users, id=user_id)
    tasks = WeeklyTask.objects.filter(user=user).order_by('date', 'time')

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_weekly_tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Day', 'Date', 'Time', 'Task'])  # CSV headers

    for task in tasks:
        writer.writerow([task.day.capitalize(), task.date, task.time, task.task])

    return response



@login_required
def view_weekly_tasks(request,user_id):

    """Fetch user's weekly tasks and render the start day page."""
    user = get_object_or_404(Users, id=user_id)
    weekly_tasks = WeeklyTask.objects.filter(user=user).order_by('date', 'time')

    if not weekly_tasks.exists():
        return render(request, "admin/dashboard/admin-view-weeklytask.html", {
            "weekly_tasks": {},
            "time_slots": [],
            "date_range": [],
        })

    time_slots = [f"{hour:02}:{minute:02}" for hour in range(00, 24) for minute in (0, 30)] 

    start_date = user.date_joined.date()
    last_task = weekly_tasks.last()

    if last_task and last_task.date:
        end_date = max(last_task.date, timezone.now().date())  # ensure it includes today
    else:
        end_date = timezone.now().date()

    # Generate list of dates
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append({
            'date': current,
            'label': current.strftime("%A"),  # Weekday name
        })
        current += timedelta(days=1)

    # Build task dict with keys like '2024-03-24_08:00'
    tasks_dict = {}
    for task in weekly_tasks:
        if task.date and task.time:
            key = f"{task.date}_{task.time.strftime('%H:%M')}" if task.time else f"{task.day}"
            tasks_dict[key] = task.task


    return render(request, "admin/dashboard/admin-view-weeklytask.html", {"weekly_tasks": tasks_dict,'date_range':date_range,"time_slots": time_slots,})