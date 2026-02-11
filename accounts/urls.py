from django.urls import path
from . import views
from buyer import views as buyer_views

urlpatterns = [
    path('resistaion/', views.resistaion_for_u_e,name = 'register'),
    path('verify-otp/', views.verify_otp,name = 'verify-otp'),
    path('complete_resistation/', views.complete_resistaion,name = 'complete_resistaion'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('logout/', views.user_logout,name='logout'),
    
]