from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from home.models import Task,WeeklyTask, ToDoTask
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from advanced_todo_core.helpers.signer import URLEncryptionDecryption
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_time
from django.forms.models import model_to_dict


# ---------------------------------------------------  Dashboard  -------------------------------------------------------------------
class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Task List'

    def get(self, request, *args, **kwargs):
        # Count tasks based on category
        self.context['total_inbox_tasks']       = Task.objects.filter(category='inbox', is_active=True).count()
        self.context['total_important_tasks']   = Task.objects.filter(category='important', is_active=True).count()
        self.context['total_urgent_tasks']      = Task.objects.filter(category='urgent', is_active=True).count()
        self.context['total_daily_tasks']       = Task.objects.filter(category='daily', is_active=True).count()
        self.context['total_weekly_tasks']      = Task.objects.filter(category='weekly', is_active=True).count()
        self.context['total_monthly_tasks']     = Task.objects.filter(category='monthly', is_active=True).count()
        self.context['total_parking_tasks']     = Task.objects.filter(category='parking', is_active=True).count()
        self.context['total_recovery_tasks']    = Task.objects.filter(category='recovery', is_active=True).count()

        # Total count of all active tasks
        self.context['total_tasks'] = Task.objects.filter(is_active=True).count()

        return render(request, "admin/home/dashboard.html", self.context)


# --------------------------------------------------- Importent Tasks  -------------------------------------------------------------------

class ImportentTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/importent-task/importent-datatable.html'    
        self.context['title'] = 'Importent Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Importent Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='important').exists()
        return data_exists
    

class LoadImportentTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='important',is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='important',is_active=False).order_by('-id')
        else:
            return Task.objects.filter(category='important').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveImportentTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class ImportentTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Importent Task'
        self.template = 'admin/home/importent-task/importent-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Importent Task", "route" : reverse('home:importent.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Importent Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'important'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:importent.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyImportentTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

# --------------------------------------------------- Urgent Tasks  -------------------------------------------------------------------

class UrgentTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/urgent-task/urgent-datatable.html'    
        self.context['title'] = 'Urgent Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Urgent Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='urgent').exists()
        return data_exists
    

class LoadUrgentTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='urgent', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='urgent', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='urgent').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveUrgentTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class UrgentTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Urgent Task'
        self.template = 'admin/home/urgent-task/urgent-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Urgent Task", "route" : reverse('home:urgent.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Urgent Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'urgent'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:urgent.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyUrgentTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


# ----------------------------------------------------------------- DAILY TASK ------------------------------------------------------------------


class DailyTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/daily-task/daily-datatable.html'    
        self.context['title'] = 'Daily Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Daily Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='daily').exists()
        return data_exists
    

class LoadDailyTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='daily', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='daily', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='daily').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveDailyTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class DailyTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Daily Task'
        self.template = 'admin/home/daily-task/daily-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Daily Task", "route" : reverse('home:daily.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Daily Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'daily'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:daily.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyDailyTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    


# ----------------------------------------------------------------- Weekly TASK ------------------------------------------------------------------


class WeeklyTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/weekly-task/weekly-datatable.html'    
        self.context['title'] = 'Weekly Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Weekly Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='weekly').exists()
        return data_exists
    

class LoadWeeklyTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='weekly', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='weekly', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='weekly').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveWeeklyTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class WeeklyTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Weekly Task'
        self.template = 'admin/home/weekly-task/weekly-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Weekly Task", "route" : reverse('home:weekly.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Weekly Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'weekly'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:weekly.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyWeeklyTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

# ----------------------------------------------------------------- Monthly TASK ------------------------------------------------------------------


class MonthlyTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/monthly-task/monthly-datatable.html'    
        self.context['title'] = 'monthly Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Monthly Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='monthly').exists()
        return data_exists
    

class LoadMonthlyTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='monthly', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='monthly', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='monthly').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveMonthlyTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class MonthlyTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Monthly Task'
        self.template = 'admin/home/monthly-task/monthly-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Monthly Task", "route" : reverse('home:monthly.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Monthly Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'monthly'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:monthly.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyMonthlyTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    


# ----------------------------------------------------------------- Parkinglot TASK ------------------------------------------------------------------


class ParkingLotTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/parkinglot-task/parkinglot-datatable.html'    
        self.context['title'] = 'Parking Lot Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Parking Lot Task", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='parkinglot').exists()
        return data_exists
    

class LoadParkingLotTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='parkinglot', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='parkinglot', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='parkinglot').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveParkingLotTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class ParkingLotTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Parking Lot Task'
        self.template = 'admin/home/parkinglot-task/parkinglot-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Parking Lot Task", "route" : reverse('home:parkinglot.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Parking Lot ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'monthly'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:parkinglot.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyParkingLotTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    


# ----------------------------------------------------------------- Recovery TASK ------------------------------------------------------------------


class RecoveryTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home/recovery-task/recovery-datatable.html'    
        self.context['title'] = 'Recovery Task'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "RecoveryTask", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = Task.objects.filter(category='recovery').exists()
        return data_exists
    

class LoadRecoveryTaskDatatable(BaseDatatableView):
    model = Task
    order_columns = ['id','headline','is_active'] 
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(category='recovery', is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(category='recovery', is_active=False).order_by('-id')
        else:
       
            return Task.objects.filter(category='recovery').order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(headline__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'headline'      : escape(item.headline),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveRecoveryTasks(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Task.objects.get(id = instance_id)
            if instance_id:
                instance.is_active = not instance.is_active
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class RecoveryTaskCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Parking Lot Task'
        self.template = 'admin/home/recovery-task/recovery-task-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Task, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Recovery Task", "route" : reverse('home:recovery.task.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Recovery Task ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Task, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Task()

            instance.headline     = request.POST.get('headline',None)
            instance.description  = request.POST.get('description',None)
            instance.category = 'monthly'

            instance.created_by   = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully: {self.action}")
            
        except Exception as e:
            error_message = f"Something went wrong. {str(e)}"
            messages.error(request, error_message)
            self.context['instance'] = form_data
            self.context['err_message'] = error_message
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:recovery.task.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyRecoveryTaskRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Task.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
# ---------------------------------------------------  Start Day  -------------------------------------------------------------------
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
            # Check if it's an update or new task
            if 'task_id' in data and data['task_id']:
                task = get_object_or_404(WeeklyTask, id=data['task_id'])
                task.task = data['task']
                task.save()
            else:
                task = WeeklyTask.objects.create(
                    user=user,
                    day=data['day'],
                    time=parse_time(data['time']),
                    task=data['task']
                )
        else:
            # Handle To-Do tasks
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