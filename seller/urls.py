from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('car_details/', views.car_details, name='car_details'),
    
    #Dashboard
    path('dashboard/overal_view/', views.dashboard, name='dashboard'),
    path('dashboard/sold_car_view/', views.sold_car_view, name='sold_car_view'),
    path('dashboard/toggle-car-status/<int:car_id>/',views.toggle_car_avalibility,name = 'toggle_car_avalibility'),
    #car detail curd
    path('dashboard/detail_view/', views.detail_view, name='detail_view'),
    path('dashboard/edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('dashboard/delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('dashboard/uploded_image_view/', views.uploded_image_view, name='uploded_image_view'),
    path('dashboard/uploded_image_edit/<int:image_id>/', views.uploaded_image_edit, name='uploded_image_edit'),
    path('dashboard/uploded_image_delete/<int:image_id>/', views.uploaded_image_delete, name='uploded_image_delete'),

    #image curd
    path('car_details/image_upload/<int:car_id>/', views.image_upload, name='image_upload'),
    path('nearby-cars/', views.nearby_cars, name='nearby_cars'),
]
