from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser   # ✅ NOT string
        fields = [
            'username',
            'email',
            'phone',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'age',
        ]
