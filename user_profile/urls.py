from django.urls import path
from . import views

urlpatterns = [

    path('', views.profile_view, name="profile"),
    path('delete-profile/', views.delete_profile, name='delete_profile'),

]