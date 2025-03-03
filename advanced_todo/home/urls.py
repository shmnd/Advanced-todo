from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'home'

urlpatterns = [

    path('', login_required(views.HomeView.as_view()), name= 'dashboard'),


    re_path(r'^important-tasks/', include([
        path('', login_required(views.ImportentTaskView.as_view()), name='importent.task.view.index'),
        path('load_importent_task_datatable', login_required(views.LoadImportentTaskDatatable.as_view()), name='importent.task.datatable'),
        path('active/', login_required(views.ActiveInactiveImportentTasks.as_view()), name="active.or.inactive.importent.task"),
        path('create/',login_required(views.ImportentTaskCreateOrUpdateView.as_view()), name='importent.task.create'),
        path('<str:id>/update/', login_required(views.ImportentTaskCreateOrUpdateView.as_view()), name='importent.task.update'),
        path('destroy_records/', login_required(views.DestroyImportentTaskRecordsView.as_view()), name='importent.task.records.destroy'),

    ])),

    re_path(r'^urgent-tasks/', include([
        path('', login_required(views.UrgentTaskView.as_view()), name='urgent.task.view.index'),
        path('load_urgent_task_datatable', login_required(views.LoadUrgentTaskDatatable.as_view()), name='urgent.task.datatable'),
        path('active/', login_required(views.ActiveInactiveUrgentTasks.as_view()), name="active.or.inactive.urgent.task"),
        path('create/',login_required(views.UrgentTaskCreateOrUpdateView.as_view()), name='urgent.task.create'),
        path('<str:id>/update/', login_required(views.UrgentTaskCreateOrUpdateView.as_view()), name='urgent.task.update'),
        path('destroy_records/', login_required(views.DestroyUrgentTaskRecordsView.as_view()), name='urgent.task.records.destroy'),

    ]))
]