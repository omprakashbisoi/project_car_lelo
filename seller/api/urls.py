
from django.urls import path

from seller.api.views import SellerCarAPIView

urlpatterns = [
    path("cars/", SellerCarAPIView.as_view(), name="api_car_list"),
]