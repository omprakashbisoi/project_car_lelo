from rest_framework import serializers
from seller.models import CarDetail, ImageStore

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = ("car_image",)

class BuyerCarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    car_location = serializers.StringRelatedField()

    class Meta:
        model = CarDetail
        fields = [
            "id",
            "seller",
            "brand",
            "car_model",
            "variant",
            "year",
            "reg_state",
            "kilometers",
            "fuel_type",
            "price",
            "is_sold",
            "is_available",
            "car_location",
            "images",
        ]


