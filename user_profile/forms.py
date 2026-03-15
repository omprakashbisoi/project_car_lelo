from django import forms
from .models import Profile, Location



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "bio"]


class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["city", "state", "pin", "address"]