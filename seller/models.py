from django.db import models
from django.conf import settings





BRAND_CHOICES = [
    ('Maruti Suzuki','Maruti Suzuki'),
    ('Hyundai','Hyundai'),
    ('Tata Motors','Tata Motors'),
    ('Mahindra','Mahindra'),
    ('Toyota','Toyota'),
    ('Kia','Kia'),
    ('Volkswagen','Volkswagen'),
    ('Honda','Honda'),
    ('Skoda','Skoda'),
    ('MG Motor','MG Motor'),
]

FUEL_CHOICES = [
    ('Petrol','Petrol'),
    ('Diesel','Diesel'),
    ('CNG','CNG'),
    ('Electric','Electric'),
]

STATE_CHOICES = [
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
]

YEAR_CHOICES = [(year, year) for year in range(2010, 2027)]

KILOMETER_CHOICES = [
    ('Up to 10,000 km','Up to 10,000 km'),
    ('10,000 - 20,000 km','10,000 - 20,000 km'),
    ('20,000 - 30,000 km','20,000 - 30,000 km'),
    ('30,000 - 40,000 km','30,000 - 40,000 km'),
    ('40,000 - 50,000 km','40,000 - 50,000 km'),
    ('50,000 - 60,000 km','50,000 - 60,000 km'),
    ('60,000 - 70,000 km','60,000 - 70,000 km'),
    ('70,000 - 80,000 km','70,000 - 80,000 km'),
    ('80,000 - 90,000 km','80,000 - 90,000 km'),
    ('90,000 - 1,00,000 km','90,000 - 1,00,000 km'),
    ('1,00,000 - 1,50,000 km','1,00,000 - 1,50,000 km'),
    ('1,50,000 - 2,00,000 km','1,50,000 - 2,00,000 km'),
    ('Above 2,00,000 km','Above 2,00,000 km'),
]


def image_upload_path(instance, filename):
    username = instance.car.seller.username
    brand = instance.car.brand.replace(' ', '_')
    return f"{username}/{brand}/{filename}"

# MODEL

class CarDetail(models.Model):

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    car_model = models.CharField(max_length=100)
    variant = models.CharField(max_length=100, blank=True)

    year = models.IntegerField(choices=YEAR_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)

    kilometers = models.CharField(max_length=50, choices=KILOMETER_CHOICES)
    reg_state = models.CharField(max_length=50, choices=STATE_CHOICES)
    car_location = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField(max_length=500, blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller.username} -- {self.brand} {self.car_model}"

# MULTIPLE IMAGE MODEL

class ImageStore(models.Model):

    car = models.ForeignKey(
        CarDetail,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image for {self.car.seller.username}-{self.car.brand}"

