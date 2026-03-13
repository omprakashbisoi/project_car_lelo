from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        
        return email



from django import forms

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        error_messages={
            'required': 'OTP field cannot be blank.',
            'min_length': 'OTP must be 6 digits.',
            'max_length': 'OTP must be 6 digits.'
        }
    )



class CompleteRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'phone',
            'first_name',
            'last_name',
            'age',
            'password1',
            'password2',
        ]
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EmailForm(forms.Form):
    email = forms.CharField(max_length=100)

class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
