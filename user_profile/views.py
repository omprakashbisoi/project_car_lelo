from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from location.models import Location
from location.utils import get_lat_lon
from .forms import ProfileUpdateForm,LocationUpdateForm
from  orders.models import Order
from accounts.models import CustomUser


@login_required
def profile_view(request):
    profile = request.user
    orders = Order.objects.filter(user=request.user)

    if not profile.location:
        location = Location.objects.create()
        profile.location = location
        profile.save()
    else:
        location = profile.location

    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        location_form = LocationUpdateForm(request.POST, instance=location)

        if profile_form.is_valid() and location_form.is_valid():
            location = location_form.save(commit=False)

            lat, lon = get_lat_lon(location.city, location.state, location.pin)
            if lat and lon:
                location.latitude = lat
                location.longitude = lon

            location.save()

            profile = profile_form.save(commit=False)
            profile.location = location
            profile.save()

            return redirect("profile")

    else:
        profile_form = ProfileUpdateForm(instance=profile)
        location_form = LocationUpdateForm(instance=location)

    return render(request, "user_profile/profile_view.html", {
        "profile_form": profile_form,
        "profile": profile,
        "location_form": location_form,
        "location": location,
        "orders": orders,
    })

@login_required
def delete_profile(request):
    profile = get_object_or_404(CustomUser, user=request.user)

    if request.method == "POST":
        profile.delete()
        return redirect('profile_view')
    return redirect('profile_view')

