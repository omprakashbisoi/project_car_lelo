from django.contrib import admin

# Register your models here.
# notification/admin.py

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'buyer',
        'seller',
        'car',
        'request_type',
        'status',
        'visible_to',
        'is_read',
        'created_at',
    ]

    list_filter = [
        'request_type',
        'status',
        'visible_to',
        'is_read',
        'created_at',
    ]

    search_fields = [
        'buyer__username',
        'seller__username',
        'car__brand',
        'car__car_model',
        'message',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    raw_id_fields = [
        'buyer',
        'seller',
        'car',
        'parent_request',
        'action_taken_by',
    ]

    ordering = ['-created_at']

    list_per_page = 25