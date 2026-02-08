from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('car_details/', views.car_details, name='car_details'),
    path('car_details/<int:car_id>/image/', views.image_upload, name='image_upload'),

    path('dashboard/overal_view/<int:user_id>/', views.dashboard, name='dashboard'),
    #car detail curd
    path('dashboard/detail_view/<int:user_id>/', views.detail_view, name='detail_view'),
    path('dashboard/edit_car/<int:user_id>/', views.edit_car, name='edit_car'),
    path('dashboard/delete_car/<int:user_id>/', views.delete_car, name='delete_car'),

    #image curd
    path('dashboard/uploded_image_view/<int:user_id>/', views.uploded_image_view, name='uploded_image_view'),
]
