from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from seller.models import CarDetail

# Create your views here.
@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('car')

    context = {
        "wishlist": wishlist
    }

    return render(request, "wishlist/wishlist_view.html", context)
@login_required
def add_remove_wish(request,car_id):
    car = get_object_or_404(CarDetail,id = car_id)
    wishlist_item,create = Wishlist.objects.get_or_create(user = request.user,car = car)
    if not create:
        wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))
    
    
