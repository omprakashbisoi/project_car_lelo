from django.shortcuts import render,redirect,get_object_or_404
from seller.models import CarDetail
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from .models import Order
# Create your views here.
@login_required
def order_view(request):
    orders = Order.objects.filter(user=request.user)
    context ={
        "orders":orders,
    }
    return render(request, 'order/order_view.html', context)
