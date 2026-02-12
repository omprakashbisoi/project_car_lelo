from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.resistaion_for_u_e, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('complete-registration/', views.complete_resistaion, name='complete_registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forget-password/<int:user_id>', views.user_logout, name='forget_password'),
    path('profile-view/', views.profile_view, name='profile_view'),
]
