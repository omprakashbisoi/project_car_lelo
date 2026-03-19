from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm,LocationUpdateForm
from location.models import Location
from location.utils import get_lat_lon
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Location
from .forms import ProfileUpdateForm, LocationUpdateForm


@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if hasattr(profile, 'profile_location') and profile.profile_location:
        location = profile.profile_location
    else:
        location = Location.objects.create()
        profile.profile_location = location
        profile.save()
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        location_form = LocationUpdateForm(
            request.POST,
            instance=location
        )
        print(profile_form.errors)
        print(location_form.errors)
        if profile_form.is_valid() and location_form.is_valid():
            location = location_form.save(commit=False)
            lat,lon = get_lat_lon(location.city, location.state, location.pin)
            if lat and lon:
                location.latitude = lat
                location.longitude = lon
            location.save()
            profile = profile_form.save(commit=False)
            profile.profile_location = location
            profile.save()
            return redirect("profile")

    else:
        profile_form = ProfileUpdateForm(instance=profile)
        location_form = LocationUpdateForm(instance=location)

    context = {
        "user": user,
        "profile_form": profile_form,
        "profile": profile,
        "location_form": location_form,
        "location": location,
    }

    return render(request, "user_profile/profile_view.html", context)
@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        profile.delete()
        return redirect('profile_view')
    return redirect('profile_view')

