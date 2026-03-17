from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm,LocationUpdateForm
from location.models import Location

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