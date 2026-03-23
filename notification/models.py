from django.db import models
from django.conf import settings
from seller.models import CarDetail

User = settings.AUTH_USER_MODEL

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

REQUEST_TYPE = [
    ('contact_request', 'Contact Request'),
    ('buy_request', 'Buy Request'),
    ('contact_shared', 'Contact Shared'),
    ('buy_confirmation', 'Buy Confirmation'),
    ('sell_confirmation', 'Sell Confirmation'),
]

VISIBLE_TO_CHOICES = [
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
    ('both', 'Both'),
]


class Notification(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    car = models.ForeignKey(
        CarDetail,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    parent_request = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
    )

    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

    visible_to = models.CharField(
        max_length=10,
        choices=VISIBLE_TO_CHOICES,
        default='both'
    )

    action_taken_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notification_actions'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.buyer} -> {self.seller} ({self.request_type} | {self.status})"