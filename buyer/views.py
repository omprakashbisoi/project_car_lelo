from seller.models import CarDetail,ImageStore
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
# Create your views here.

# Create your tests here.
def buyer(request):
    cars = CarDetail.objects.filter(is_available=True)
    context = {
        'cars':cars,
        # 'image':image,
    }
    return render(request,"buyer/car_showcase.html",context)


from django.db.models import Q

def search(request):
    keyword = request.GET.get('keyword','')

    cars = CarDetail.objects.filter(is_available=True)
    if keyword:
        car = cars.filter(
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
