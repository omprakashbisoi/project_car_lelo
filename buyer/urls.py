from django.urls import path
from . import views

urlpatterns = [
    path('',views.buyer,name = 'buyer'),
    path('search/',views.search,name = 'search'),
]