from django.urls import path
from . import views

urlpatterns = [
    path("cars/",views.BuyerCarAPIView.as_view(), name="buyer_car_api_view"),
    path("cars/<int:car_id>/", views.BuyerCarDetailAPIView.as_view(), name="buyer_car_detail_api_view"),
]
