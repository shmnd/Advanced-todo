import json
import csv
from django.utils.timezone import now,localdate,make_aware,localtime
from django.shortcuts import get_object_or_404, render, get_object_or_404,redirect
from django.views import View
from home.models import WeeklyTask, ToDoTask, Note, ChecklistItem,Reminder
from authentication.models import Users 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_time
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime
from django.db import models
from django.db.models import Q 
from django.contrib import messages


# Start Day View
class StartDayView(LoginRequiredMixin, View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Start Day'

    def get(self, request, *args, **kwargs):
        # Fetch weekly tasks and to-do tasks
        weekly_tasks = WeeklyTask.objects.filter(user=request.user).values()
        todo_tasks = ToDoTask.objects.filter(user=request.user).values()

        # Pass tasks to context
        self.context['weekly_tasks'] = list(weekly_tasks)
        self.context['todo_tasks'] = list(todo_tasks)

        # Render the template with context
        return render(request, "admin/home/start-day.html", self.context)


# API: Get Tasks
@method_decorator(csrf_exempt, name='dispatch')
class GetTasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Convert `time` field to string in `HH:MM` format
        weekly_tasks = WeeklyTask.objects.filter(user=user)
        weekly_tasks_list = [
            {**model_to_dict(task), 'time': task.time.strftime('%H:%M')}
            for task in weekly_tasks
        ]

        # Fetch To-Do tasks as well
        todo_tasks = ToDoTask.objects.filter(user=user).values()
        
        return JsonResponse({
            'weekly_tasks': weekly_tasks_list,
            'todo_tasks': list(todo_tasks),
        })

# API: Add Task
@method_decorator(csrf_exempt, name='dispatch')
class AddTaskView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user

        # Check task type
        if data['type'] == 'weekly':
            if 'task_id' in data and data['task_id']:
                task = WeeklyTask.objects.filter(id=data['task_id']).first()

                if task and localdate(task.created_at) == localdate():
                    # Update the existing task only if it was created today
                    task.task = data['task']
                    task.save()
                else:
                    # Create a new task if the date is different or task_id is invalid
                    task = WeeklyTask.objects.create(
                        user=user,
                        day=data['day'],
                        time=parse_time(data['time']),
                        task=data['task']
                    )
            else:
                # Create a new task if no task_id is provided
                task = WeeklyTask.objects.create(
                    user=user,
                    day=data['day'],
                    time=parse_time(data['time']),
                    task=data['task']
                )
        else:
            # Handle To-Do tasks similarly
            if 'task_id' in data and data['task_id']:
                task = ToDoTask.objects.filter(id=data['task_id']).first()

                if task and localdate(task.created_at) == localdate():
                    task.task = data['task']
                    task.save()
                else:
                    task = ToDoTask.objects.create(
                        user=user,
                        task_type=data['task_type'],
                        task=data['task']
                    )
            else:
                task = ToDoTask.objects.create(
                    user=user,
                    task_type=data['task_type'],
                    task=data['task']
                )

        # Return JSON response with task ID
        return JsonResponse({'status': 'success', 'task_id': task.id})



# API: Delete Task
@method_decorator(csrf_exempt, name='dispatch')
class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id, *args, **kwargs):
        task_type = request.GET.get('type')
        if task_type == 'weekly':
            WeeklyTask.objects.filter(id=task_id).delete()
        else:
            ToDoTask.objects.filter(id=task_id).delete()
        return JsonResponse({'status': 'deleted'})

# API: Update Task
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id, *args, **kwargs):
        data = json.loads(request.body)
        task_type = request.GET.get('type')
        if task_type == 'weekly':
            task = get_object_or_404(WeeklyTask, id=task_id)
            task.task = data['task']
            task.save()
        else:
            task = get_object_or_404(ToDoTask, id=task_id)
            task.task = data['task']
            task.save()
        return JsonResponse({'status': 'updated'})
    

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
        "Admin Assigned": Note.objects.filter(assigned_to=request.user).distinct(),
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
    if not request.user.is_staff:
        messages.error(request, "Unauthorized Admin")
        return redirect('home:startday')

    users = Users.objects.filter(is_staff=False)
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
    if request.method == "POST" and request.user.is_staff:
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
    weekly_tasks = WeeklyTask.objects.filter(user=user_id).order_by('date', 'time')

    time_slots = [f"{hour:02}:{minute:02}" for hour in range(00, 24) for minute in (0, 30)] 

    tasks_dict = {}
    for task in weekly_tasks:
        key = f"{task.day}_{task.time.strftime('%H:%M')}" if task.time else f"{task.day}"
        tasks_dict[key] = task.task

    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

    return render(request, "admin/dashboard/admin-view-weeklytask.html", {"weekly_tasks": tasks_dict,'weekdays':weekdays,"time_slots": time_slots,})