from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarDetailForm,ImageUploadForm,LocationForm
from .models import CarDetail,ImageStore
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from location.utils import get_lat_lon
from django.contrib import messages
from django.db.models import F
from django.db.models.functions import ACos, Cos, Sin, Radians

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
        car_form = CarDetailForm(request.POST)
        location_form = LocationForm(request.POST)
        if car_form.is_valid() and location_form.is_valid():

            try:

                # ---- LOCATION ----
                location = location_form.save(commit=False)

                # Validate input
                if location.city and location.state and location.pin:
                    lat, lng = get_lat_lon(
                        location.city,
                        location.state,
                        location.pin
                    )

                    # Safe assignment
                    if lat and lng:
                        location.latitude = lat
                        location.longitude = lng

                location.save()

                    # ---- CAR ----
                car = car_form.save(commit=False)
                car.seller = request.user
                car.car_location = location
                car.save()
                request.user.role = 'seller'
                request.user.save()
                messages.success(request, "Car added successfully")
                return redirect('image_upload', car_id=car.id)

            except Exception as e:
                print("Error:", e)
                messages.error(request, "Something went wrong. Try again.")

    else:
        car_form = CarDetailForm()
        location_form = LocationForm()

    context = {
        'car_form': car_form,
        'location_form': location_form,
    }

    return render(request, 'seller/car_detail.html', context)


@login_required
def dashboard(request):
    user = request.user
    cars = CarDetail.objects.filter(seller=user)
    car_count = cars.count()
    sold_car_count = cars.filter(is_sold=True).count()
    context={
        'car_count':car_count,
        'sold_car_count':sold_car_count,
    }
    return render(request,'seller/dashboard/dashboard.html',context)


def detail_view(request):
    cars = CarDetail.objects.filter(seller=request.user)
    context = {
        'cars': cars,
    }

    return render(request, 'seller/dashboard/car_detail_view.html', context)

from django.http import JsonResponse

def toggle_car_avalibility(request, car_id):
    if request.method == "POST":
        car = get_object_or_404(CarDetail, id=car_id, seller=request.user)
        
        car.is_available = not car.is_available
        car.save()

        return JsonResponse({
            'success': True,
            'is_available': car.is_available,
        })

    return JsonResponse({'success': False})


@login_required
def edit_car(request,car_id):
    car = get_object_or_404(CarDetail,pk=car_id)

    if car.seller != request.user:
        messages.error(request,"You are not allowed to edit this car")
        return redirect('seller')

    if request.method == "POST":
        form = CarDetailForm(request.POST,request.FILES,instance=car)
        if form.is_valid():
            updated_car = form.save()
            messages.success(request,"Car updated successfully")
            return redirect('detail_view')
    else:
        form = CarDetailForm(instance=car)

    context = {
        'car':car,
        'form':form,
    }
    return render(request,'seller/dashboard/edit_car_details.html',context)


@login_required
def delete_car(request,car_id):
    car = get_object_or_404(CarDetail,pk=car_id)

    if car.seller != request.user:
        messages.error(request,"You are not allowed to delete this car")
        return redirect('seller')

    ImageStore.objects.filter(car=car).delete()
    car.delete()
    messages.success(request,"Car deleted successfully")

    return redirect('detail_view')


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
        return redirect('buyer')

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES, instance=image)

        if form.is_valid():
            form.save()
            messages.success(request, "Image updated successfully")
            return redirect('uploded_image_view')

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

def near_by_car(request):
    user = request.user
    profile = user.profile
    if not hasattr(profile, 'profile_location') or not profile.profile_location:
        messages.warning(request, "Please update your location to see nearby cars.")
        return render(request, "nearby_cars.html", {"cars": [], "location_missing": True})
    location = profile.profile_location
    if not location.latitude or not location.longitude:
        messages.warning(request, "Please update your location to see nearby cars.")
        return render(request, "nearby_cars.html", {"cars": [], "location_missing": True})
    user_lat  = location.latitude
    user_lon = location.longitude
    from django.contrib import messages

def nearby_cars(request):
    user = request.user
    profile = user.profile

    if not hasattr(profile, 'profile_location') or not profile.profile_location:
        messages.warning(request, "Please update your location to see nearby cars.")
        return render(request, "nearby_cars.html", {"cars": [], "location_missing": True})

    location = profile.profile_location

    if not location.latitude or not location.longitude:
        messages.warning(request, "Please complete your location details.")
        return render(request, "nearby_cars.html", {"cars": [], "location_missing": True})

    user_lat = location.latitude
    user_lon = location.longitude

    cars = CarDetail.objects.filter(
        car_location__latitude__isnull=False,
        car_location__longitude__isnull=False
    ).annotate(
        distance=6371 * ACos(
            Cos(Radians(user_lat)) *
            Cos(Radians(F('car_location__latitude'))) *
            Cos(Radians(F('car_location__longitude')) - Radians(user_lon)) +
            Sin(Radians(user_lat)) *
            Sin(Radians(F('car_location__latitude')))
        )
    ).order_by('distance')

    return render(request, "seller/nearby_cars.html", {"cars": cars})