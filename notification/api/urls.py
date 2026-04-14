from django.urls import path

from notification.api.views import (
    BaseNotificationAPIView,
    MarkAsReadAPIView,
    NotificationActionAPIView,
    NotificationCreateAPIView,
)

urlpatterns = [
    path("", BaseNotificationAPIView.as_view(), name="notification_api_list"),
    path("create/<int:car_id>/<str:request_type>/", NotificationCreateAPIView.as_view(), name="notification_api_create"),
    path("action/<int:req_id>/<str:action>/", NotificationActionAPIView.as_view(), name="notification_api_action"),
    path("mark-as-read/", MarkAsReadAPIView.as_view(), name="notification_api_mark_as_read"),
]
