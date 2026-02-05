from django.contrib.auth import logout,login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def home(request):
    return render(request,"home.html")
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   
            username = request.POST['username']
            email = request.POST['email']
            subject = "Welcome to our car lelo platform 🚗"
            message = f"""
            Hi {username},

            Your account has been successfully created.

            You can now log in and explore the platform.

            Thanks,
            Team Car Lelo
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            auth.login(request,user)
            return redirect('home')
    else:
        form = RegistrationForm
    context = {
        'form':form,
    }
    return render(request,"register.html",context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not  None:
                login(request,user)
                print(f"{username} is login")
                return redirect('home')
            else:
                print(f"{username} login failed") 
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request,'login.html',context)



def user_logout(request):
    logout(request)
    return redirect('login')
