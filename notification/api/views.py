from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.models import Notification
from seller.models import CarDetail
from orders.models import Order
from notification.api.serializers import (
    BaseNotificationSerializer,
    NotificationCreateSerializer,
    MarkAsReadSerializer,
)


class BaseNotificationAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BaseNotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            Q(buyer=user, visible_to__in=["buyer", "both"]) |
            Q(seller=user, visible_to__in=["seller", "both"])
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

class NotificationActionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, req_id, action, *args, **kwargs):
        if action not in ["accepted", "rejected"]:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        notif = get_object_or_404(Notification, id=req_id)

        if notif.seller != request.user:
            return Response(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        if notif.status != "pending":
            return Response(
                {"detail": "This request has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            notif.status = action
            notif.is_read = True
            notif.action_taken_by = request.user
            notif.save(update_fields=["status", "is_read", "action_taken_by", "updated_at"])

            if notif.request_type == "contact_request":
                if action == "accepted":
                    msg = f"Seller shared contact: {notif.seller.email}"
                    req_type = "contact_shared"
                else:
                    msg = "Seller rejected your contact request."
                    req_type = "contact_request"

                Notification.objects.create(
                    buyer=notif.buyer,
                    seller=notif.seller,
                    car=notif.car,
                    parent_request=notif,
                    request_type=req_type,
                    status=None,
                    message=msg,
                    visible_to="buyer",
                    is_read=False
                )

            elif notif.request_type == "buy_request":
                if action == "accepted":
                    Order.objects.create(
                        user=notif.buyer,
                        car=notif.car,
                        car_name=f"{notif.car.brand} {notif.car.car_model}",
                        car_price=notif.car.price,
                        seller_name=str(notif.seller),
                        status="completed",
                    )

                    notif.car.is_sold = True
                    notif.car.is_available = False
                    notif.car.sold_at = timezone.now()
                    notif.car.save(update_fields=["is_sold", "is_available", "sold_at"])

                    buyer_msg = f"Seller accepted your buy request for {notif.car.brand} {notif.car.car_model}."
                    seller_msg = f"You confirmed sale of {notif.car.brand} {notif.car.car_model} to {notif.buyer.username}."

                    Notification.objects.create(
                        buyer=notif.buyer,
                        seller=notif.seller,
                        car=notif.car,
                        parent_request=notif,
                        request_type="buy_confirmation",
                        status=None,
                        message=buyer_msg,
                        visible_to="buyer",
                        is_read=False
                    )

                    Notification.objects.create(
                        buyer=notif.buyer,
                        seller=notif.seller,
                        car=notif.car,
                        parent_request=notif,
                        request_type="sell_confirmation",
                        status=None,
                        message=seller_msg,
                        visible_to="seller",
                        is_read=False
                    )

                else:
                    Notification.objects.create(
                        buyer=notif.buyer,
                        seller=notif.seller,
                        car=notif.car,
                        parent_request=notif,
                        request_type="buy_request",
                        status=None,
                        message=f"Your buy request for {notif.car.brand} {notif.car.car_model} was rejected.",
                        visible_to="buyer",
                        is_read=False
                    )

        return Response(
            {"detail": f"Request {action} successfully."},
            status=status.HTTP_200_OK
        )
class MarkAsReadAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MarkAsReadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification_ids = serializer.validated_data.get("notification_ids", [])
        mark_all = serializer.validated_data.get("mark_all", False)

        if mark_all:
            notifications = Notification.objects.filter(
                Q(buyer=request.user, visible_to__in=["buyer", "both"]) |
                Q(seller=request.user, visible_to__in=["seller", "both"]),
                is_read=False
            )
        else:
            notifications = Notification.objects.filter(
                (Q(buyer=request.user, visible_to__in=["buyer", "both"]) |
                Q(seller=request.user, visible_to__in=["seller", "both"])),
                id__in=notification_ids,
                is_read=False
            )

        updated_count = notifications.update(is_read=True)

        return Response(
            {"detail": f"{updated_count} notifications marked as read."},
            status=status.HTTP_200_OK
        )
