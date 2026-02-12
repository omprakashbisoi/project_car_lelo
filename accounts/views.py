from django.shortcuts import render,redirect
from django.http import HttpResponse
from .utils import generate_otp
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm,CompleteRegistrationForm,OTPVerificationForm,LoginForm
from django.contrib import auth
from django.contrib.auth import authenticate, login,logout
# Create your views here.

def resistaion_for_u_e(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = generate_otp()
            expiry = timezone.now() + timedelta(minutes=5)
            try:
                otp_obj = EmailOTP.objects.get(email=email)

                # If already exists → check resend limit
                if otp_obj.resend_count >= 3:
                    return render(
                        request,
                        'accounts/resistation.html',
                        {'form': form, 'error': "Resend limit reached"}
                    )

                otp_obj.resend_count += 1

            except EmailOTP.DoesNotExist:
                # First time → create new record
                otp_obj = EmailOTP(
                    email=email,
                    resend_count=1
                )
            otp_obj.otp = otp
            otp_obj.expiry_time = expiry
            otp_obj.is_verified = False
            otp_obj.save()


            send_mail(
                subject='Your OTP code',
                message=f'Your OTP is {otp}. It is valid for 5 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            request.session['pending_email'] = email
            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(request, "accounts/resistation.html", {'form': form})




def verify_otp(request):
    email = request.session.get('pending_email')

    if not email:
        return redirect('registration')

    if request.method == "POST":
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            user_otp = form.cleaned_data['otp']

            try:
                otp_obj = EmailOTP.objects.get(email=email)
            except EmailOTP.DoesNotExist:
                return render(
                    request,
                    "accounts/verify_otp.html",
                    {'form': form, 'error': "Invalid Email"}
                )

            if otp_obj.is_expired():
                return render(
                    request,
                    "accounts/verify_otp.html",
                    {'form': form, 'error': "OTP expired"}
                )

            if otp_obj.otp != user_otp:
                return render(
                    request,
                    "accounts/verify_otp.html",
                    {'form': form, 'error': "Invalid OTP"}
                )

            
            otp_obj.is_verified = True
            otp_obj.save()

            
            request.session['verified_email'] = email
            del request.session['pending_email']

            return redirect('complete_registration')

    else:
        form = OTPVerificationForm()

    return render(request, "accounts/verify_otp.html", {'form': form})



def complete_resistaion(request):

    verified_email = request.session.get('verified_email')

    if not verified_email:
        return redirect('registration')

    if request.method == "POST":
        form = CompleteRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = verified_email

            user.save()

            # Clean session
            del request.session['verified_email']

            # Send welcome mail
            subject = "Welcome to Car Lelo 🚗"
            message = f"""
Hi {user.first_name},

Your account has been successfully created.

Welcome to Car Lelo!
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            auth.login(request, user)

            return redirect('buyer')

    else:
        form = CompleteRegistrationForm()

    return render(
        request,
        'accounts/complete_registration.html',
        {'form': form}
    )
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('buyer')
            else:
                return render(request,"accounts/login.html",{'form': form, 'error': "Invalid credentials"})     
    else:
        form = LoginForm()
    return render(request,'accounts/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

def forget_password(request,user_id):
    pass

def profile_view(request):
    return render(request,'accounts/profile_view.html')