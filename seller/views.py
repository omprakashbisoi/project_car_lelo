from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarDetailForm
from .models import CarDetail,ImageStore


# Create your views here.
def seller(request):
    cars = CarDetail.objects.filter(seller=request.user)
    context = {
        'cars':cars,
    }
    return render(request,'seller/seller.html',context)
def car_details(request):
    if request.method == "POST":
        form = CarDetailForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect("image_upload",car.id)
    else:
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

def dashboard(request,user_id):
    car_count = CarDetail.objects.filter(seller=user_id).count()
    context={
        'car_count':car_count,
    }
    return render(request,'seller/dashboard/dashboard.html',context)

from django.shortcuts import get_object_or_404

def detail_view(request, user_id):
    cars = CarDetail.objects.filter(seller_id=user_id)

    context = {
        'cars': cars,
    }

    return render(request, 'seller/dashboard/car_detail_view.html', context)

def edit_car(request,user_id):
    car = get_object_or_404(CarDetail,pk= user_id)
    if request.method == "POST":
        form = CarDetailForm(request.POST,request.FILES,instance=car)
        if form.is_valid():
            updated_car = form.save()
            return redirect('detail_view')
    else:
        form = CarDetailForm(instance=car)
    context = {
        'car':car,
        'form':form,
    }
    return render(request,'seller/dashboard/edit_car_details.html',context)

def delete_car(request,user_id):
    car = get_object_or_404(CarDetail,pk= user_id)
    ImageStore.objects.filter(car=car).delete()
    car.delete()
    return redirect('detail_view')

def uploded_image_view(request,user_id):
    images = ImageStore.objects.filter(car__seller_id=user_id)

    context = {
        'images': images,
    }
    return render(request,'seller/dashboard/image_uploaded_view.html',context)