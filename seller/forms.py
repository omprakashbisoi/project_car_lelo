
from django import forms
 
from .models import CarDetail,ImageStore

class CarDetailForm(forms.ModelForm):
    class Meta:
        model = CarDetail
        fields = "__all__"
class ImageUpload(forms.ModelForm):
    class Meta:
        model = ImageStore
        fields = ('image',)
    
 