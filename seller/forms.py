
from django import forms
from .models import CarDetail,ImageStore

class CarDetailForm(forms.ModelForm):
    class Meta:
        model = CarDetail
        exclude = ("seller",)
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageStore
        fields = ("image","img_type",)
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 5 * 1040 * 1040 :
                raise forms.ValidationError("Image size must be under 5MB")
        return image
    
        
    

 