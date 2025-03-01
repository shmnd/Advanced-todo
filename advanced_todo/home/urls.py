from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'home'

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name= 'dashboard'),
]