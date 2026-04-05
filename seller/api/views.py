
from rest_framework import generics
from rest_framework.permissions import AllowAny

from seller.api.serializers import CarSerializer
from seller.models import CarDetail


class SellerCarAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CarSerializer
    queryset = CarDetail.objects.select_related("seller", "car_location").order_by("-created_at")
