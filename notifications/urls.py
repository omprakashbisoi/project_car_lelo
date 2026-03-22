from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.base_notifications, name='base_notifications'),
    path('send/<int:car_id>/', views.send_request, name='send_request'),

    path('seller-notifications/', views.seller_notification, name='seller_notification'),
    path('buyer-notifications/', views.buyer_notification, name='buyer_notification'),

    path('accept/<int:req_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:req_id>/', views.reject_request, name='reject_request'),

    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),
]