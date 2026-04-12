from django.urls import path
from rest_framework.routers import DefaultRouter
from seller.api.views import (
    ImageUploadAPIView,
    LocationAPIView,
    SellCarDetailAPIView,
    SellerDashboardCarViewSet,
    SellerDashboardImageViewSet,

)

router = DefaultRouter()
router.register(r"dashboard/cars", SellerDashboardCarViewSet, basename="seller-dashboard-cars")
router.register(r"dashboard/images", SellerDashboardImageViewSet, basename="seller-dashboard-images")

urlpatterns = [
    path("sell-car/", SellCarDetailAPIView.as_view(), name="sell_car_api"),
    path("sell-car/location/<int:car_id>/", LocationAPIView.as_view(), name="location_api"),
    path("sell-car/image-upload/<int:car_id>/", ImageUploadAPIView.as_view(), name="image_upload_api"),
]

urlpatterns += router.urls
