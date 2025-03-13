from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'home'

urlpatterns = [

    path('', login_required(views.StartDayView.as_view()), name='startday'),
    
    re_path(r'^task/', include([
        path('api/get-tasks/', login_required(views.GetTasksView.as_view()), name='get_tasks'),
        path('api/add-task/', login_required(views.AddTaskView.as_view()), name='add_task'),
        path('api/delete-task/<int:task_id>/', login_required(views.DeleteTaskView.as_view()), name='delete_task'),
        path('api/update-task/<int:task_id>/', login_required(views.UpdateTaskView.as_view()), name='update_task'), 
    ])),

    re_path(r'^cards/', include([
        path('', views.note_page, name='note-page'),
        path('api/notes/', login_required(views.NoteListView.as_view()), name='note-list'),
        path('api/notes/<int:note_id>/', login_required(views.NoteDetailView.as_view()), name='note-detail'),
        path('api/notes/<int:note_id>/items/', login_required(views.ChecklistItemView.as_view()), name='checklist-add'),
        path('api/notes/<int:note_id>/items/<int:item_id>/', login_required(views.ChecklistItemView.as_view()), name='checklist-modify'),

        path('api/notes/<int:note_id>/pin/', views.toggle_pin, name='toggle_pin'),
      
    ])),
]


