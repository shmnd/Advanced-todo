from django.contrib.auth import login,logout,authenticate
from authentication.models import Users
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.conf import settings
from advanced_todo_core.helpers.hash import Hash
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
import random
from django.urls import reverse


class UserRegisterView(View):
    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    template_name = "admin/authentication/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            # Check if email exists
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"status_code": 200, "message": "Email already exists."}, status=400)

            # Check if username exists
            if Users.objects.filter(username=username).exists():
                return JsonResponse({"status_code": 200, "message": "Username already exists."}, status=400)

            # Check if passwords match
            if password != confirm_password:
                return JsonResponse({"status_code": 200, "message": "Passwords do not match."}, status=400)

            # Create User
            user = Users.objects.create(
                email=email,
                username=username,
                password=make_password(password),
                is_active=True,
            )

            login_url = reverse("authentication:login")  
            return JsonResponse({
                "status_code": 100,
                "message": "Signup successful! Redirecting to login...",
                "redirect_url": login_url  # ✅ Include redirect URL
            }, status=200)
            
        except Exception as e:
            # ✅ Return error details in response
            return JsonResponse({
                "status_code": 500,
                "message": "Something went wrong.",
                "error": str(e)
            }, status=500)



class UserLoginView(View):

    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verified:
            pass
            # return redirect('home:dashboard')
        return render(request, 'admin/authentication/login.html')

    def post(self, request):
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)

            EMAIL_HOST_USER = settings.EMAIL_HOST_USER

            if user is not None:
                otp = str(random.randint(100000,999999))
                hash_otp = Hash.bcrypt({'key':str(otp)})
                user.otp = hash_otp 
                user.otp_expiry = timezone.now() + timedelta(minutes=3)
                user.is_verified = False
                user.save(update_fields=['otp','is_verified','otp_expiry'])

                request.session['user_id'] = user.id

                try:
                    send_mail(
                        "Your OTP for Verification",
                        f"Hello {user.username},\n\nYour OTP for verification is: {otp}\n\nThis OTP is valid for 3 minutes.",
                        EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    ...

                self.response_format['message'] = 'Otp send sucessfully'
                self.response_format['status_code'] = 100

            else:
                self.response_format['message'] = 'Invalid Email or Password'
        except Exception as e:
            self.response_format['message'] = "Something went wrong, Please try again later"
            self.response_format['errors'] = str(e)

        return JsonResponse(self.response_format,status=200)
    


class OtpVerificationView(View):

    def get(self,request,*args, **kwargs):
        return render(request,'admin/authentication/otp.html')

    def get(self,request,*args, **kwargs):
        otp = request.POST.get('otp')
        user_id = request.POST.get('user_id')

        if not user_id:
            messages.error(request,'User not found, Please login again')
            return redirect('authentication:login')
        
        user = Users.objects.get(id=user_id)

        if Hash.verify(user.otp,otp):
            user.is_verified = True
            user.save()
            login(request,user)
            return redirect('home:dashboard')
        else:
            messages.error(request,'Invalid Otp , Please try again later')
            return render(request,'admin/authentication/otp.html')
        

def signout(request):
    logout(request)
    return redirect('authentication:login')