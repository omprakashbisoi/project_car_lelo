from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('car_details/', views.car_details, name='car_details'),
    path('<int:car_id>/image/', views.image_upload, name='image_upload'),
]
