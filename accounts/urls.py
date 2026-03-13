from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.resistaion_for_u_e, name='register'),
    path('email/verify-otp/', views.email_verify_otp, name='email_verify_otp'),
    path('complete-registration/', views.complete_resistaion, name='complete_registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile-view/', views.profile_view, name='profile_view'),
    path('forget-password/', views.forget_password_email_verification, name='forget_password'),
    path('password/verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path("resend-otp/", views.resend_otp, name="resend_otp")
]
