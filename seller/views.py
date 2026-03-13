from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarDetailForm,ImageUploadForm
from .models import CarDetail,ImageStore
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def seller(request):
    cars = CarDetail.objects.filter(seller=request.user)
    context = {
        'cars':cars,
    }
    return render(request,'seller/seller.html',context)


@login_required
def car_details(request):
    if request.method == "POST":
        form = CarDetailForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()
            messages.success(request,"Car added successfully")
            return redirect('image_upload',car_id = car.id)
    else:
        form = CarDetailForm()

    context = {
        'form':form,
    }
    return render(request,'seller/car_detail.html',context)


@login_required
def dashboard(request,user_id):
    car_count = CarDetail.objects.filter(seller=user_id).count()
    context={
        'car_count':car_count,
    }
    return render(request,'seller/dashboard/dashboard.html',context)


def detail_view(request, user_id):
    cars = CarDetail.objects.filter(seller_id=user_id)

    context = {
        'cars': cars,
    }

    return render(request, 'seller/dashboard/car_detail_view.html', context)


@login_required
def edit_car(request,user_id):
    car = get_object_or_404(CarDetail,pk=user_id)

    if car.seller != request.user:
        messages.error(request,"You are not allowed to edit this car")
        return redirect('seller')

    if request.method == "POST":
        form = CarDetailForm(request.POST,request.FILES,instance=car)
        if form.is_valid():
            updated_car = form.save()
            messages.success(request,"Car updated successfully")
            return redirect('detail_view',user_id=request.user.id)
    else:
        form = CarDetailForm(instance=car)

    context = {
        'car':car,
        'form':form,
    }
    return render(request,'seller/dashboard/edit_car_details.html',context)


@login_required
def delete_car(request,user_id):
    car = get_object_or_404(CarDetail,pk=user_id)

    if car.seller != request.user:
        messages.error(request,"You are not allowed to delete this car")
        return redirect('seller')

    ImageStore.objects.filter(car=car).delete()
    car.delete()
    messages.success(request,"Car deleted successfully")

    return redirect('detail_view',user_id=request.user.id)


@login_required
def image_upload(request, car_id):

    car = get_object_or_404(CarDetail, id=car_id, seller=request.user)

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            img_type = form.cleaned_data.get("img_type")

            exist_img = ImageStore.objects.filter(
                car=car,
                img_type=img_type
            ).first()

            if exist_img:
                exist_img.image.delete(save=False)
                exist_img.delete()

            image_obj = form.save(commit=False)
            image_obj.car = car
            image_obj.save()

            messages.success(request, "Image uploaded successfully")

            return redirect("uploded_image_view")

    else:
        form = ImageUploadForm()

    context = {
        "form": form,
        "car": car
    }

    return render(request, "seller/image_upload.html", context)

@login_required
def uploded_image_view(request):
    cars = CarDetail.objects.filter(seller=request.user).prefetch_related("images")

    context = {
        'cars': cars,
    }
    return render(request,'seller/dashboard/image_uploaded_view.html',context)


@login_required
def uploaded_image_edit(request, image_id):

    image = get_object_or_404(ImageStore, pk=image_id)

    if image.car.seller != request.user:
        messages.error(request, "You are not allowed to edit this image")
        return redirect('seller')

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES, instance=image)

        if form.is_valid():
            form.save()
            messages.success(request, "Image updated successfully")
            return redirect('seller')

    else:
        form = ImageUploadForm(instance=image)

    context = {
        "form": form,
        "image": image
    }

    return render(request, 'seller/dashboard/image_edit.html', context)


@login_required
def uploaded_image_delete(request, image_id):

    image = get_object_or_404(ImageStore, pk=image_id)

    if image.car.seller != request.user:
        messages.error(request, "You are not allowed to delete this image")
        return redirect('seller')

    if request.method == "POST":
        image.image.delete(save=False)
        image.delete()
        messages.success(request, "Image deleted successfully")

    return redirect("uploded_image_view")