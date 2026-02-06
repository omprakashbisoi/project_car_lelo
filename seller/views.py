from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarDetailForm
from .models import CarDetail,ImageStore


# Create your views here.
def seller(request):
    return render(request,'seller/seller.html')
def car_details(request):
    form = CarDetailForm()
    context = {
        'form':form,
    }
    return render(request,'seller/car_detail.html',context)
def image_upload(request,car_id):
    car = get_object_or_404(CarDetail,id = car_id)
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            ImageStore.objects.create(car=car,image = image)
        return redirect('seller')
    return render(request, 'seller/image_upload.html', {'car': car})