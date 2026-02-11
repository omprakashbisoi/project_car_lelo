from django.shortcuts import render,redirect
from .utils import generate_otp
from .models import EmailOTP,
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .forms import ResistationForm,CompleteResistaionForm,OTPVarificationForm
# Create your views here.

def resistaion(request):
    if request.method == "POST":
        pass
    else:
        form = ResistationForm()
    context = {
        'form':form,
    }
    return redirect(request,'accounts/resistation.html',context)

def complete_resistaion(request):
    if request.method == "POST":
        pass
    else:
        form = CompleteResistaionForm()
    context = {
        'form':form,
    }
    return redirect(request,'accounts/complete_registration.html',context)




def send_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = generate_otp()
        expiry = timezone.now()+timedelta(minutes=5)
        otp_obj,create = EmailOTP.objects.get_or_create(email=email)
        if not create and otp_obj.resend_count >=3:
            return render(request,"send_otp_html",{'error':"Resend limit is reached"})
        otp_obj.otp = otp
        otp_obj.expiry_time = expiry
        otp_obj.is_verified = False
        otp_obj.save()
        send_mail(
            subject='Your OTP code',
            message=f'Your OTP is {otp}.It is valid till 5 min.Do not share if with any one',
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return render(request, "verify_otp.html", {"email": email})
    else:
        form = OTPVarificationForm()
    return render(request, "send_otp.html")

def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user_otp = request.POST.get('otp')
        try:
            otp_obj = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            return render(request,"verify_otp.html",{'error':"invalid Email"})
        if otp_obj.is_expired():
            return render(request,"verify_otp.html",{'error':"OTP expired"})
        if otp_obj.otp != user_otp:
            return render(request,"verify_otp.html",{'error':"Invalid OTP"})
        otp_obj.is_verified = True
        otp_obj.save()
        request.session['Verified_email'] = email
        return redirect('complete_registration')
    return render(request, "verify_otp.html")

def resistaoin