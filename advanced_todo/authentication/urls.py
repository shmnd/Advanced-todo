from django.urls import path, re_path
from . import views
from authentication import views
app_name = 'authentication'

urlpatterns = [
    path("signup/", views.UserRegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('otp/', views.OtpVerificationView.as_view(), name='otp'),

    re_path(r'^logout',views.signout,name='logout')
]