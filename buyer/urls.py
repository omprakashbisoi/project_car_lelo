from django.urls import path
from . import views

urlpatterns = [
    path('',views.buyer,name = 'buyer'),
    path('search/',views.search,name = 'search'),
    path('car-detail-view/<int:car_id>/',views.car_detail_view,name='car_detail_view'),
]