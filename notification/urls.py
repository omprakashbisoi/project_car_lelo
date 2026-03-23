from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.base_notifications, name='base_notifications'),
    path('contact-request/<int:car_id>/', views.contact_request, name='contact_request'),
    path('buy-request/<int:car_id>/', views.buy_request, name='buy_request'),
    path('request-action/<int:req_id>/<str:action>/', views.handle_request_action, name='handle_request_action'),
    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),
]