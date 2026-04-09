from rest_framework import serializers
from location.models import Location
from seller.models import CarDetail, ImageStore


class SellCarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetail
        exclude = ("seller", "sold_at", "is_sold", "is_available", "created_at", "updated_at")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "city", "state", "pin", "address", "latitude", "longitude")


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = ("car_image", "img_type")

    def validate_car_image(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be under 5MB.")
        return value


class SellerDashboardCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetail
        fields = "__all__"
        read_only_fields = ("seller", "created_at", "updated_at", "sold_at")


class SellerDashboardImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = ("id", "car_image", "img_type", "car")
        read_only_fields = ("car",)

    def validate_car_image(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be under 5MB.")
        return value
