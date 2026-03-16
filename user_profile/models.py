import os
import uuid
from pathlib import Path
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from seller.models import CarDetail


def image_upload_path(instance, filename):

    username = instance.user.username
    file_extension = os.path.splitext(filename)[1]

    unique_filename = f"{uuid.uuid4()}{file_extension}"

    return f"profile/{username}/{unique_filename}"


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True
    )

    bio = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.image and not self.image.name.endswith(".webp"):

            img = Image.open(self.image)

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

            filename = Path(self.image.name).stem

            self.image.save(
                f"{filename}.webp",
                ContentFile(buffer.read()),
                save=False
            )

            img.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
