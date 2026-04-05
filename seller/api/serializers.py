
from rest_framework import serializers

from seller.models import CarDetail


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetail
        exclude = ("sold_at",)
