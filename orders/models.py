from django.db import models
from django.conf import settings
from seller.models import CarDetail
from django.core.validators import RegexValidator
# ---------------- STATUS CHOICES ---------------- #

BOOKING_STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]

ORDER_STATUS = [
    ('initiated', 'Initiated'),
    ('pending', 'Pending Payment'),
    ('paid', 'Paid'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

# ---------------- BOOKING MODEL ---------------- #

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    car = models.ForeignKey(
        CarDetail,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    mobile = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10 digit PIN code')],
        blank=True
    )

    booking_date = models.DateField()
    booking_time = models.TimeField()

    message = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'car', 'booking_date']  # prevent spam

    def __str__(self):
        return f"{self.user} booked {self.car}"


# ---------------- ORDER MODEL ---------------- #

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    car = models.ForeignKey(
        CarDetail,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )

    # 🔥 LINK TO BOOKING (IMPORTANT)
    booking = models.OneToOneField(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 🔥 SNAPSHOT FIELDS
    car_name = models.CharField(max_length=255)
    car_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller_name = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='initiated'
    )

    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-fill snapshot data
        if self.car:
            self.car_name = str(self.car)
            self.car_price = self.car.price
            self.seller_name = str(self.car.seller)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user}"