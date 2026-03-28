import os
import uuid
from pathlib import Path
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from location.models import Location
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from location.models import Location
from django.core.validators import RegexValidator

def image_upload_path(instance, filename):

    username = instance.user.username
    file_extension = os.path.splitext(filename)[1]

    unique_filename = f"{uuid.uuid4()}{file_extension}"

    return f"profile/{username}/{unique_filename}"

ROLE = (
    ('admin', 'Admin'),
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)

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
    
    location = models.OneToOneField(Location,on_delete=models.CASCADE,blank=True,null=True)

    bio = models.TextField(blank=True, null=True)

    profile_image = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):

        if self.profile_image and not self.profile_image.name.endswith(".webp"):

            img = Image.open(self.profile_image)

            allowed_formats = ["JPEG", "PNG", "WEBP"]

            if img.format not in allowed_formats:
                raise ValidationError("Unsupported image format")

            if img.height > 1200 or img.width > 1200:
                img.thumbnail((1200, 1200))

            img = img.convert("RGB")

            buffer = BytesIO()

            img.save(
                buffer,
                format="WEBP",
                optimize=True,
                quality=80
            )

            buffer.seek(0)

            filename = Path(self.profile_image.name).stem

            self.profile_image.save(
                f"{filename}.webp",
                ContentFile(buffer.read()),
                save=False
            )

            img.close()

        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.username


class EmailOTP(models.Model):
    email = models.EmailField(unique=True,db_index=True)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()
    resend_count = models.PositiveIntegerField(default=0)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expiry_time

    def __str__(self):
        return self.email

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()
    resend_count = models.PositiveIntegerField(default=0)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_expired(self):
        return timezone.now() > self.expiry_time
    def __str__(self):
        return f"{self.user.username} OTP"
