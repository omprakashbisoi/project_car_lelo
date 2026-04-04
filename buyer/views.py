from seller.models import CarDetail,ImageStore
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from seller.models import CarDetail,ImageStore
from location.models import Location
from wishlist.models import Wishlist
# Create your views here.

def buyer(request):
    cars = CarDetail.objects.filter(is_available=True).prefetch_related('images')

    wishlist_car_ids = set()
    if request.user.is_authenticated:
        wishlist_car_ids = set(
            Wishlist.objects.filter(user=request.user)
            .values_list('car_id', flat=True)
        )

    context = {
        'cars': cars,
        'wishlist_car_ids': wishlist_car_ids,
    }
    return render(request, "buyer/car_showcase.html", context)

def search(request):
    keyword = request.GET.get('keyword', '').strip()

    cars = CarDetail.objects.filter(is_available=True)

    if keyword:
        cars = cars.filter(
            Q(brand__icontains=keyword) |
            Q(car_model__icontains=keyword) |
            Q(variant__icontains=keyword) |
            Q(fuel_type__icontains=keyword)
        )

    context = {
        'cars': cars,
        'keyword': keyword
    }

    return render(request, 'buyer/search.html', context)

def car_detail_view(request, car_id):
    car = get_object_or_404(CarDetail, id=car_id)
    imgs = ImageStore.objects.filter(car=car)
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, car=car).exists()
    return render(request, 'buyer/car_detail_view_p.html', {
        "car": car,
        "imgs": imgs,
        "is_wishlisted":is_wishlisted,
    })





