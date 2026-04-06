from django.urls import path
from . import views

urlpatterns = [
    path("cars/",views.BuyerCarAPIView.as_view(), name="buyer_car_api_view"),
]