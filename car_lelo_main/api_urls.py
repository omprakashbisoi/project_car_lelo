
from django.urls import include, path
from wishlist.api_views import WishlistApiView

urlpatterns = [
    path("seller/", include("seller.api.urls")),
    path("buyer/", include("buyer.api.urls")),
    path("notification/", include("notification.api.urls")),
    path("account/", include("accounts.api.urls")),
    path("orders/", include("orders.api.urls")),
    path("wishlist/<int:car_id>/", WishlistApiView.as_view(), name="wishlist_api"),
]
