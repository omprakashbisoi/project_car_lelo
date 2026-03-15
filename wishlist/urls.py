from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add_remove_wish/<int:car_id>/', views.add_remove_wish, name='add_remove_wish'),
]