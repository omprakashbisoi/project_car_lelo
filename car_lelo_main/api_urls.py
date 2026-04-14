
from django.urls import include, path

urlpatterns = [
    path("seller/", include("seller.api.urls")),
    path("buyer/", include("buyer.api.urls")),
    path("notification/", include("notification.api.urls")),
]
