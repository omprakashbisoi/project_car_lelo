
from django.urls import include, path

urlpatterns = [
    path("", include("seller.api.urls")),
]
