from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'home'

urlpatterns = [

    path('', views.StartDayView.as_view(), name='startday'),
    path('api/get-tasks/', views.GetTasksView.as_view(), name='get_tasks'),
    path('api/add-task/', views.AddTaskView.as_view(), name='add_task'),
    path('api/delete-task/<int:task_id>/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('api/update-task/<int:task_id>/', views.UpdateTaskView.as_view(), name='update_task'), 

    path('dashboard/', login_required(views.HomeView.as_view()), name= 'dashboard'),


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
    ])),

    re_path(r'^daily-tasks/', include([
        path('', login_required(views.DailyTaskView.as_view()), name='daily.task.view.index'),
        path('load_daily_task_datatable', login_required(views.LoadDailyTaskDatatable.as_view()), name='daily.task.datatable'),
        path('active/', login_required(views.ActiveInactiveDailyTasks.as_view()), name="active.or.inactive.daily.task"),
        path('create/',login_required(views.DailyTaskCreateOrUpdateView.as_view()), name='daily.task.create'),
        path('<str:id>/update/', login_required(views.DailyTaskCreateOrUpdateView.as_view()), name='daily.task.update'),
        path('destroy_records/', login_required(views.DestroyDailyTaskRecordsView.as_view()), name='daily.task.records.destroy'),
    ])),

    re_path(r'^weekly-tasks/', include([
        path('', login_required(views.WeeklyTaskView.as_view()), name='weekly.task.view.index'),
        path('load_weekly_task_datatable', login_required(views.LoadWeeklyTaskDatatable.as_view()), name='weekly.task.datatable'),
        path('active/', login_required(views.ActiveInactiveWeeklyTasks.as_view()), name="active.or.inactive.weekly.task"),
        path('create/',login_required(views.WeeklyTaskCreateOrUpdateView.as_view()), name='weekly.task.create'),
        path('<str:id>/update/', login_required(views.WeeklyTaskCreateOrUpdateView.as_view()), name='weekly.task.update'),
        path('destroy_records/', login_required(views.DestroyWeeklyTaskRecordsView.as_view()), name='weekly.task.records.destroy'),
    ])),

    re_path(r'^monthly-tasks/', include([
        path('', login_required(views.MonthlyTaskView.as_view()), name='monthly.task.view.index'),
        path('load_monthly_task_datatable', login_required(views.LoadMonthlyTaskDatatable.as_view()), name='monthly.task.datatable'),
        path('active/', login_required(views.ActiveInactiveMonthlyTasks.as_view()), name="active.or.inactive.monthly.task"),
        path('create/',login_required(views.MonthlyTaskCreateOrUpdateView.as_view()), name='monthly.task.create'),
        path('<str:id>/update/', login_required(views.MonthlyTaskCreateOrUpdateView.as_view()), name='monthly.task.update'),
        path('destroy_records/', login_required(views.DestroyMonthlyTaskRecordsView.as_view()), name='monthly.task.records.destroy'),
    ])),

    re_path(r'^parkinglot-tasks/', include([
        path('', login_required(views.ParkingLotTaskView.as_view()), name='parkinglot.task.view.index'),
        path('load_parkinglot_task_datatable', login_required(views.LoadParkingLotTaskDatatable.as_view()), name='parkinglot.task.datatable'),
        path('active/', login_required(views.ActiveInactiveParkingLotTasks.as_view()), name="active.or.inactive.parkinglot.task"),
        path('create/',login_required(views.ParkingLotTaskCreateOrUpdateView.as_view()), name='parkinglot.task.create'),
        path('<str:id>/update/', login_required(views.ParkingLotTaskCreateOrUpdateView.as_view()), name='parkinglot.task.update'),
        path('destroy_records/', login_required(views.DestroyParkingLotTaskRecordsView.as_view()), name='parkinglot.task.records.destroy'),
    ])),

    re_path(r'^recovery-tasks/', include([
        path('', login_required(views.RecoveryTaskView.as_view()), name='recovery.task.view.index'),
        path('load_recovery_task_datatable', login_required(views.LoadRecoveryTaskDatatable.as_view()), name='recovery.task.datatable'),
        path('active/', login_required(views.ActiveInactiveRecoveryTasks.as_view()), name="active.or.inactive.recovery.task"),
        path('create/',login_required(views.RecoveryTaskCreateOrUpdateView.as_view()), name='recovery.task.create'),
        path('<str:id>/update/', login_required(views.RecoveryTaskCreateOrUpdateView.as_view()), name='recovery.task.update'),
        path('destroy_records/', login_required(views.DestroyRecoveryTaskRecordsView.as_view()), name='recovery.task.records.destroy'),
    ])),
]
