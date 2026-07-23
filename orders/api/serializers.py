from rest_framework import serializers

from orders.models import Booking, Order
from seller.models import CarDetail


class BookingSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(
        queryset=CarDetail.objects.filter(is_available=True, is_sold=False)
    )

    class Meta:
        model = Booking
        fields = (
            "id",
            "car",
            "mobile",
            "booking_date",
            "booking_time",
            "message",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "status", "created_at")

    def validate_car(self, car):
        request = self.context.get("request")
        if request and car.seller == request.user:
            raise serializers.ValidationError("You cannot book your own car.")
        return car

    def create(self, validated_data):
        return Booking.objects.create(user=self.context["request"].user, **validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "car",
            "booking",
            "car_name",
            "car_price",
            "seller_name",
            "status",
            "payment_id",
            "payment_status",
            "created_at",
        )
        read_only_fields = fields
