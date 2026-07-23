from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.api.serializers import BookingSerializer, OrderSerializer
from orders.models import Booking, Order


class BookingListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("car").order_by("-created_at")


class BookingDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    lookup_url_kwarg = "booking_id"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("car")


class OrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("car", "booking").order_by("-created_at")


class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("car", "booking")
