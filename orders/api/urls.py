from django.urls import path

from orders.api.views import (
    BookingDetailAPIView,
    BookingListCreateAPIView,
    OrderDetailAPIView,
    OrderListAPIView,
)

urlpatterns = [
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking_api_list_create"),
    path("bookings/<int:booking_id>/", BookingDetailAPIView.as_view(), name="booking_api_detail"),
    path("", OrderListAPIView.as_view(), name="order_api_list"),
    path("<int:order_id>/", OrderDetailAPIView.as_view(), name="order_api_detail"),
]
