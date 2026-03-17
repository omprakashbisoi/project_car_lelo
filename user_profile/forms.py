from django import forms
from .models import Profile
from location.models import Location


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image", "bio"]


class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["city", "state", "pin", "address"]