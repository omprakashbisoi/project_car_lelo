from django import forms
from accounts.models import CustomUser
from location.models import Location


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_image","phone"]


class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["city", "state", "pin", "address"]