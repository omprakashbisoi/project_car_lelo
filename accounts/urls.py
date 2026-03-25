from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registration_view, name='register'),
    path('email/resend-otp/', views.resend_mail_otp, name='resend_mail_otp'),
    path('email/verify-otp/', views.email_verify_otp, name='email_verify_otp'),
    path('complete-registration/', views.complete_registration, name='complete_registration'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('forgot-password/', views.forget_password_view, name='forget_password'),
    path('password/verify-otp/', views.password_verify_otp, name='password_verify_otp'),
    path('password/resend-otp/', views.resend_password_otp, name='resend_password_otp'),
    path('password/reset/', views.reset_password, name='reset_password'),

]