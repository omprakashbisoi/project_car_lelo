from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "class": "form-control"
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")

        return email


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter 6-digit OTP",
            "class": "form-control text-center",
            "maxlength": "6"
        }),
        error_messages={
            'required': 'OTP is required.',
            'min_length': 'OTP must be 6 digits.',
            'max_length': 'OTP must be 6 digits.',
        }
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')

        if not otp.isdigit():
            raise forms.ValidationError("OTP must contain only numbers.")

        return otp


class CompleteRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

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

    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old.")

        return age



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control"
        })
    )


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your registered email",
            "class": "form-control"
        })
    )


class NewPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "New Password",
            "class": "form-control"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": "form-control"
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

            if len(password) < 6:
                raise forms.ValidationError("Password must be at least 6 characters.")

        return cleaned_data