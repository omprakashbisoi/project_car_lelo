from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from buyer.api.serializers import BuyerCarSerializer
from seller.models import CarDetail


class BuyerCarAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BuyerCarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["brand", "fuel_type", "reg_state", "year", "is_available", "is_sold"]
    search_fields = ["brand", "car_model", "variant", "fuel_type", "reg_state"]
    ordering_fields = ["created_at", "price", "year"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return CarDetail.objects.filter(
            is_available=True,
        ).select_related(
            "seller", "car_location"
        ).prefetch_related(
            "images"
        )


class BuyerCarDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BuyerCarSerializer
    lookup_url_kwarg = "car_id"

    def get_queryset(self):
        return CarDetail.objects.filter(
            is_available=True,
        ).select_related(
            "seller", "car_location"
        ).prefetch_related(
            "images"
        )
