from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

 
ROLE = (
    ('admin', 'Admin'),
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)
from django.core.validators import RegexValidator
class CustomUser(AbstractUser):

    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{10}$',
            message="Phone number must be exactly 10 digits."
        )]
    )

    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE, default='buyer')

    age = models.PositiveIntegerField(null=True, blank=True)

    first_name = models.CharField(max_length=40,blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.username

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()
    resend_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expiry_time

    def __str__(self):
        return self.email


