from rest_framework import serializers
from notification.models import Notification


class BaseNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "buyer",
            "seller",
            "car",
            "parent_request",
            "request_type",
            "status",
            "message",
            "is_read",
            "visible_to",
            "action_taken_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "buyer",
            "seller",
            "car",
            "parent_request",
            "request_type",
            "status",
            "visible_to",
            "action_taken_by",
            "created_at",
            "updated_at",
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["message"]


class NotificationActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accepted", "rejected"])
    message = serializers.CharField(required=False, allow_blank=True, max_length=500)


class MarkAsReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
    )
    mark_all = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if not attrs.get("mark_all") and not attrs.get("notification_ids"):
            raise serializers.ValidationError(
                "Provide notification_ids or set mark_all=true."
            )
        return attrs
