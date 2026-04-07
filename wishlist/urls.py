from django.urls import path
from . import views
from .api_views import WishlistApiView
urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),
    path('add_remove_wish/<int:car_id>/', views.add_remove_wish, name='add_remove_wish'),
    path('api/toggle/<int:car_id>', WishlistApiView.as_view(),name='wishlist_toggle_api')
]