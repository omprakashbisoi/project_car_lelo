from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request,"home.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

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

            auth.login(request, user)
            return redirect('buyer')
    else:
        form = RegistrationForm()

    return render(request,"register.html",{'form':form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            print(f"{user.username} is login")
            return redirect('buyer')
    else:
        form = AuthenticationForm()

    return render(request,'login.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')
