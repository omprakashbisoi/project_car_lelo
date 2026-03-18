from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
LOCATION_TYPE = [
    ('user', 'User'),
    ('car', 'Car'),
]

class Location(models.Model):
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE,
        blank=True,
    )


    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default="India", blank=True)

    pin = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$', 'Enter a valid 6 digit PIN code')],
        blank=True
    )

    address = models.CharField(max_length=255, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.city or 'Unknown'}, {self.state or 'Unknown'}"