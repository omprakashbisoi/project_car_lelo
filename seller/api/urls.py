from django.urls import path
from seller.api.views import (
    ImageUploadAPIView,
    LocationAPIView,
    SellCarDetailAPIView
)

urlpatterns = [
    path("sell-car/", SellCarDetailAPIView.as_view(), name="sell_car_api"),
    path("location/<int:car_id>/", LocationAPIView.as_view(), name="location_api"),
    path("sell-car/image-upload/<int:car_id>/", ImageUploadAPIView.as_view(), name="image_upload_api"),
]
