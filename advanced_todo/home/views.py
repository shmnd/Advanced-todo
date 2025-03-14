from django.shortcuts import get_object_or_404, render, get_object_or_404,redirect
from django.views import View
from home.models import WeeklyTask, ToDoTask, Note, ChecklistItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_time
from django.forms.models import model_to_dict
from datetime import date
from django.utils.timezone import localdate
from django.views.decorators.http import require_POST


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
    

# ---------------------------------------------------------------- TASKS -----------------------------------------------------------------------------


@login_required
def note_page(request):
    """Render the Notes Page (cards.html)"""
    return render(request, 'admin/home/cards.html')
@method_decorator(csrf_exempt, name='dispatch')
class NoteListView(View):
    """Handles fetching and creating notes"""

    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by('-is_pinned', '-id').values()
        return JsonResponse(list(notes), safe=False)

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
            note = get_object_or_404(Note, id=note_id, user=request.user)
            note.delete()
            return JsonResponse({'status': 'deleted'})
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
        
    
@login_required
@csrf_exempt  # Allow AJAX requests
@require_POST  # Only allow POST requests
def toggle_pin(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    # Toggle pin status
    note.is_pinned = not note.is_pinned
    note.save()

    return JsonResponse({'status': 'success', 'is_pinned': note.is_pinned})


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