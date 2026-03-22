from django.db import models
from django.conf import settings
from seller.models import CarDetail

User = settings.AUTH_USER_MODEL

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

class ContactRequest(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    car = models.ForeignKey(CarDetail, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} -> {self.seller} ({self.status})"