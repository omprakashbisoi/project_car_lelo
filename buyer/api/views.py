from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from buyer.api.serializers import BuyerCarSerializer
from seller.models import CarDetail

class BuyerCarAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BuyerCarSerializer

    queryset = CarDetail.objects.select_related(
        "seller", "car_location"
    ).prefetch_related(
        "images"
    ).order_by("-created_at")
