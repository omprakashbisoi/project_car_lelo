from django.urls import path
from seller.api.views import (
    ImageUploadAPIView,
    LocationAPIView,
    SellCarDetailAPIView,
    SellerDashboardCarAvailableAPIView,
    SellerDashboardCarListAPIView,
    SellerDashboardCarAPIView,
    SellerDashboardImageListAPIView,
    SellerDashboardImageAPIView,

)

urlpatterns = [
    path("sell-car/", SellCarDetailAPIView.as_view(), name="sell_car_api"),
    path("sell-car/location/<int:car_id>/", LocationAPIView.as_view(), name="location_api"),
    path("sell-car/image-upload/<int:car_id>/", ImageUploadAPIView.as_view(), name="image_upload_api"),
    path("dashboard/cars/", SellerDashboardCarListAPIView.as_view(), name="seller_dashboard_car_list_api"),
    path("dashboard/cars/<int:pk>/", SellerDashboardCarAPIView.as_view(), name="seller_dashboard_car_api"),
    path("dashboard/cars/<int:pk>/toggle-availability/", SellerDashboardCarAvailableAPIView.as_view(), name="seller_dashboard_car_available_api"),
    path("dashboard/images/", SellerDashboardImageListAPIView.as_view(), name="seller_dashboard_image_list_api"),
    path("dashboard/images/<int:pk>/", SellerDashboardImageAPIView.as_view(), name="seller_dashboard_image_api"),
]
