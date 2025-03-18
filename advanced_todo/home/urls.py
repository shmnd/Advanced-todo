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
        path('api/notes/update-order/', views.update_order, name='update_order'),

        

      
    ])),


    re_path(r'^reminders/',include([
        path('',views.reminder_page,name='reminder-page'),
        path('api/remove-reminder/<int:reminder_id>/', views.remove_reminders, name='remove_reminders'),
        path('api/notes/<int:note_id>/get-reminder/', views.get_reminder, name='get_reminder'),
        path('api/notes/<int:note_id>/set-reminder/', views.set_reminder, name='set_reminder'),
        path('api/check-reminders/', views.check_reminders, name='check_reminders'),

    ]))
]


