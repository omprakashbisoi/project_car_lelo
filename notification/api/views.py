from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.models import Notification
from seller.models import CarDetail
from notification.api.serializers import (
    BaseNotificationSerializer,
    NotificationCreateSerializer,
)


class BaseNotificationAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BaseNotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            Q(buyer=user, visible_to="buyer") |
            Q(seller=user, visible_to="seller")
        ).select_related(
            "buyer", "seller", "car", "parent_request", "action_taken_by"
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        buy_request_car_ids = list(
            Notification.objects.filter(
                buyer=request.user,
                request_type="buy_request"
            ).values_list("car_id", flat=True)
        )

        return Response({
            "notifications": serializer.data,
            "buy_request_car_ids": buy_request_car_ids,
        })


class NotificationCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationCreateSerializer

    def post(self, request, car_id, request_type, *args, **kwargs):
        if request_type not in ["contact_request", "buy_request"]:
            return Response(
                {"detail": "Invalid request type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        car = get_object_or_404(CarDetail, id=car_id)

        if car.seller == request.user:
            return Response(
                {"detail": "You cannot send a request for your own car."},
                status=status.HTTP_400_BAD_REQUEST
            )

        already_exists = Notification.objects.filter(
            buyer=request.user,
            car=car,
            request_type=request_type,
            status="pending",
        ).exists()

        if already_exists:
            return Response(
                {"detail": "You already have a pending request for this car."},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = request.data.get("message", "").strip()
        if not message:
            if request_type == "contact_request":
                message = f"Interested in your {car.brand} {car.car_model}, please share your contact information"
            else:
                message = f"I want to buy your {car.brand} {car.car_model}"

        notif = Notification.objects.create(
            buyer=request.user,
            seller=car.seller,
            car=car,
            request_type=request_type,
            status="pending",
            message=message,
            visible_to="seller",
            is_read=False,
        )

        return Response(
            {"detail": "Request created successfully.", "id": notif.id},
            status=status.HTTP_201_CREATED
        )
