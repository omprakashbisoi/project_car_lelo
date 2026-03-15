from django.db import models
from django.conf import settings
from seller.models import CarDetail


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )

    car = models.ForeignKey(
        CarDetail,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'car'],
                name='unique_user_car_wishlist'
            )
        ]

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['car']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.car.brand}"