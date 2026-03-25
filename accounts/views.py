from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

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

def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            now = timezone.now()
            otp = generate_otp()
            expiry = now + timedelta(minutes=5)
            try:
                otp_obj = EmailOTP.objects.get(email=email)
            except EmailOTP.DoesNotExist:
                otp_obj = None


            if otp_obj:
                
                if otp_obj.last_sent_at and now-otp_obj.last_sent_at > timedelta(hours=12):
                    otp_obj.resend_count=0
                    otp_obj.save()
                if otp_obj.resend_count >= 3:
                    return render(request, 'accounts/resistation.html', {
                        'form': form,
                        'error': "Resend limit reached. Try again after 12 hours."
                    })

                otp_obj.otp = otp
                otp_obj.expiry_time = expiry
                otp_obj.resend_count += 1
                otp_obj.last_sent_at = now
                otp_obj.is_verified = False

            else:
                otp_obj = EmailOTP.objects.create(
                    email=email,
                    otp=otp,
                    expiry_time=expiry,
                    resend_count=1,
                    is_verified=False
                )

            otp_obj.save()

            send_mail(
                subject='Your OTP code',
                message=f'Your OTP is {otp}. It is valid for 5 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            request.session['pending_email'] = email

            return redirect('email_verify_otp')

    else:
        form = RegistrationForm()

    return render(request, "accounts/resistation.html", {'form': form})


def resend_mail_otp(request):
    email = request.session.get('pending_email')

    if not email:
        return redirect('resistaion')

    try:
        otp_obj = EmailOTP.objects.get(email=email)
    except EmailOTP.DoesNotExist:
        return redirect('registration_view')

    now = timezone.now()

    if otp_obj.last_sent_at and now - otp_obj.last_sent_at > timedelta(hours=12):
        otp_obj.resend_count = 0

    if otp_obj.resend_count >= 3:
        return render(request, 'accounts/resistation.html', {
            'error': "Resend limit reached. Try again after 12 hours."
        })

    otp = generate_otp()

    otp_obj.otp = otp
    otp_obj.expiry_time = now + timedelta(minutes=5)
    otp_obj.resend_count += 1
    otp_obj.last_sent_at = now
    otp_obj.is_verified = False
    otp_obj.save()

    send_mail(
        subject='Your OTP code',
        message=f'Your OTP is {otp}. It is valid for 5 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )

    return redirect('email_verify_otp')


def email_verify_otp(request):
    email = request.session.get('pending_email')

    if not email:
        return redirect('register')
    
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            user_otp = form.cleaned_data['otp']

            try:
                otp_obj = EmailOTP.objects.get(email=email)
            except EmailOTP.DoesNotExist:
                return render(request, "accounts/verify_otp.html", {
                    'form': form,
                    'error': "Something went wrong. Please register again."
                })

            if otp_obj.is_expired():
                return render(request, "accounts/verify_otp.html", {
                    'form': form,
                    'error': "OTP expired"
                })

            if otp_obj.otp != user_otp:
                return render(request, "accounts/verify_otp.html", {
                    'form': form,
                    'error': "Invalid OTP"
                })

            otp_obj.is_verified = True
            otp_obj.save()

            request.session['verified_email'] = email
            del request.session['pending_email']

            return redirect('complete_registration')

    else:
        form = OTPVerificationForm()

    return render(request, "accounts/verify_otp.html", {'form': form})


def complete_registration(request):
    verified_email = request.session.get('verified_email')

    if not verified_email:
        return redirect('register')

    if request.method == "POST":
        form = CompleteRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = verified_email
            user.save()

            del request.session['verified_email']

            send_mail(
                subject="Welcome to Car Lelo 🚗",
                message=f"Hi {user.first_name}, your account is ready!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            auth.login(request, user)

            return redirect('buyer')

    else:
        form = CompleteRegistrationForm()

    return render(request, 'accounts/complete_registration.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("buyer")

            return render(request, "accounts/login.html", {
                'form': form,
                'error': "Invalid credentials"
            })

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def forget_password_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = CustomUser.objects.get(email=email)

                now = timezone.now()
                otp = generate_otp()
                expiry = now + timedelta(minutes=3)
                try:
                    otp_obj = PasswordResetOTP.objects.get(user=user)
                except PasswordResetOTP.DoesNotExist:
                    otp_obj = None

                if otp_obj:

                    if otp_obj.last_sent_at and now - otp_obj.last_sent_at > timedelta(hours=12):
                        otp_obj.resend_count = 0

                    if otp_obj.resend_count >= 3:
                        return render(request, "accounts/password_reset.html", {
                            "form": form,
                            "error": "Too many attempts. Try again after 12 hours."
                        })

                    otp_obj.otp = otp
                    otp_obj.expiry_time = expiry
                    otp_obj.resend_count += 1
                    otp_obj.last_sent_at = now
                    otp_obj.is_verified = False

                else:

                    otp_obj = PasswordResetOTP.objects.create(
                        user=user,
                        otp=otp,
                        expiry_time=expiry,
                        resend_count=1,
                        last_sent_at=now,
                    )

                otp_obj.save()

                send_mail(
                    subject='Password Reset OTP',
                    message=f'Your OTP is {otp}. Valid for 3 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )

                request.session["reset_user"] = user.id
                print("last")
            except CustomUser.DoesNotExist:
                pass

            return redirect("password_verify_otp")

    else:
        form = EmailForm()

    return render(request, "accounts/password_reset.html", {"form": form})


def password_verify_otp(request):
    user_id = request.session.get("reset_user")

    if not user_id:
        return redirect("forget_password")

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]

            try:
                otp_obj = PasswordResetOTP.objects.get(user=user)
            except PasswordResetOTP.DoesNotExist:
                otp_obj = None

            if not otp_obj:
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "Request new OTP"
                })

            if otp_obj.is_expired():
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "OTP expired"
                })

            if otp_obj.otp != entered_otp:
                return render(request, "accounts/password_reset_confirm.html", {
                    "form": form,
                    "error": "Invalid OTP"
                })

            otp_obj.is_verified = True
            otp_obj.save()

            request.session["otp_verified"] = True

            return redirect("reset_password")

    else:
        form = OTPVerificationForm()

    return render(request, "accounts/password_reset_confirm.html", {"form": form})




def resend_password_otp(request):
    user_id = request.session.get("reset_user")

    if not user_id:
        return redirect("login")

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect("login")

    try:
        otp_obj = PasswordResetOTP.objects.get(user=user)
    except PasswordResetOTP.DoesNotExist:
        otp_obj = None

    if not otp_obj:
        return redirect("forget_password")

    now = timezone.now()

    if otp_obj.last_sent_at and now - otp_obj.last_sent_at > timedelta(hours=12):
        otp_obj.resend_count = 0

    if otp_obj.resend_count >= 3:
        return render(request, "accounts/password_reset_confirm.html", {
            "error": "Try again after 12 hours."
        })

    otp = generate_otp()
    expiry = now + timedelta(minutes=3)

    otp_obj.otp = otp
    otp_obj.expiry_time = expiry
    otp_obj.resend_count += 1
    otp_obj.last_sent_at = now
    otp_obj.is_verified = False
    otp_obj.save()

    send_mail(
        subject="Password Reset OTP",
        message=f"Your new OTP is {otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return redirect('password_verify_otp')

def reset_password(request):
    if not request.session.get("otp_verified"):
        return redirect('forget_password')

    user_id = request.session.get('reset_user')
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = NewPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password != confirm_password:
                return render(request, "accounts/password_reset_complete.html", {
                    "form": form,
                    "error": "Passwords do not match"
                })

            user.set_password(password)
            user.save()

            send_mail(
                subject='Password Changed',
                message='Your password was changed successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            # CLEAN SESSION
            del request.session["reset_user"]
            del request.session["otp_verified"]

            return redirect("login")

    else:
        form = NewPasswordForm()

    return render(request, "accounts/password_reset_complete.html", {"form": form})

