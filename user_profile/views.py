from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, LocationUpdateForm
from .models import Profile, Location


@login_required
def profile_view(request):

    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)
    location, created = Location.objects.get_or_create(profile=profile)

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

        if profile_form.is_valid() and location_form.is_valid():
            profile_form.save()
            location_form.save()

            return redirect("profile")

    else:

        profile_form = ProfileUpdateForm(instance=profile)
        location_form = LocationUpdateForm(instance=location)

    context = {
        "user": user,
        "profile_form": profile_form,
        "location_form": location_form,
        "profile": profile,
        "location": location,
    }

    return render(request, "user_profile/profile_view.html", context)