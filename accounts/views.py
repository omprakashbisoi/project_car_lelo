from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from .utils import generate_otp
from .models import EmailOTP, CustomUser, PasswordResetOTP
from .forms import (
    RegistrationForm,
    CompleteRegistrationForm,
    OTPVerificationForm,
    LoginForm,
    EmailForm,
    NewPasswordForm
)
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




def email_verify_otp(request):
    email = request.session.get('pending_email')

    if not email:
        return redirect('resistaion_for_u_e')

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
from django.utils import timezone
from datetime import timedelta

def forget_password_email_verification(request):

    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = CustomUser.objects.get(email=email)

                last_otp = PasswordResetOTP.objects.filter(user=user).last()

                if last_otp and last_otp.resend_count >= 3:
                    return render(
                        request,
                        "accounts/login.html",
                        {'form': form, 'error': 'Resend limit reached'}
                    )

                otp = generate_otp()
                expiry = timezone.now() + timedelta(minutes=3)

                otp_obj = PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp,
                    expiry_time=expiry,
                )

                otp_obj.resend_count += 1
                otp_obj.save()

                send_mail(
                    subject='Password Reset OTP',
                    message=f'Your OTP is {otp}. It is valid for 3 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )

                request.session["reset_user"] = user.id

                return redirect("verify_otp")

            except CustomUser.DoesNotExist:
                form.add_error("email", "Email not registered")

    else:
        form = EmailForm()

    return render(request, "accounts/password_reset.html", {"form": form,})




from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import OTPVerificationForm
from .models import PasswordResetOTP
from .models import CustomUser

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import OTPVerificationForm
from .models import PasswordResetOTP, CustomUser

def verify_otp(request):
    reset_user_id = request.session.get("reset_user")
    if not reset_user_id:
        return redirect("forgot_password")

    user = CustomUser.objects.get(id=reset_user_id)

    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]

            last_otp = PasswordResetOTP.objects.filter(user=user).last()
            if not last_otp:
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "No OTP found. Please request a new OTP."
                })

            # Cooldown check
            if last_otp.resend_count >= 3:
                cooldown_time = last_otp.created_at + timedelta(hours=2)
                if timezone.now() < cooldown_time:
                    return render(request, "accounts/password_reset_confirm.html", {
                        "form": form,
                        "error": "Resend limit reached. Try again after 2 hours."
                    })

            # Expiry check
            if last_otp.is_expired():
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "OTP has expired. Please request a new one."
                })

            # OTP match
            if last_otp.otp != entered_otp:
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "Invalid OTP entered."
                })

            # OTP correct
            last_otp.is_verified = True
            last_otp.save()
            request.session["otp_verified"] = True
            return redirect("reset_password")
        else:
            # Form invalid (blank)
            return render(request, "accounts/password_reset_confirm.html", {
                "form": form,
                "error": "OTP field cannot be blank."
            })
    else:
        form = OTPVerificationForm()

    return render(request, "accounts/password_reset_confirm.html", {"form": form})

def resend_otp(request):
    reset_user = request.session.get("reset_user")
    if not request.session.get("reset_user"):
        return redirect("login")
    user = CustomUser.objects.get(id=reset_user)
    otp_obj = PasswordResetOTP.objects.filter(user=user).last()
    if not otp_obj:
        return redirect("forget_password")
    if otp_obj.resend_count >= 3:
        cooldown_time = otp_obj.created_at + timedelta(hours=2)
        if timezone.now() < cooldown_time:
            return render(
                request,
                "accounts/password_reset_confirm.html",
                {
                    "error": "Resend limit reached. Try again after 2 hours."
                }
            )
        else:
            # reset counter after cooldown
            otp_obj.resend_count = 0
    otp = generate_otp()
    otp_obj.otp = otp
    otp_obj.expiry_time = timezone.now() + timedelta(minutes=3)
    otp_obj.resend_count += 1
    otp_obj.created_at = timezone.now()

    otp_obj.save()



    send_mail(
        subject="Password Reset OTP",
        message=f"Your new OTP is {otp}. It is valid for 3 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


    request.session["otp_timer_reset"] = True

    return redirect('verify_otp')
def reset_password(request):
    if request.session.get("otp_verified"):
        return redirect('login')

    user_id = request.session.get('reset_user')

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":

        form = NewPasswordForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password != confirm_password:

                return render(request,
                    "accounts/password_reset_confirm.html",
                    {"form": form, "error": "Passwords do not match"}
                )
            user.set_password(password)
            user.save()
            email = user.email
            send_mail(
                subject='Password Changed Successfully',
                message='Your password has been changed successfully. If you did not perform this action, please contact support immediately.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect("login")

    else:
        form = NewPasswordForm()

    return render(request,
        "accounts/password_reset_complete.html",
        {"form": form,}
    )

            
def profile_view(request):
    return render(request,'accounts/profile_view.html')