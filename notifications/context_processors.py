from .models import ContactRequest

def notification_data(request):
    if request.user.is_authenticated:

        notifications = ContactRequest.objects.filter(
            seller=request.user
        ).order_by('-created_at')

        unread_count = notifications.filter(is_read=False).count()
        recent_notifications = notifications[:5]

    else:
        unread_count = 0
        recent_notifications = []

    return {
        'unread_count': unread_count,
        'recent_notifications': recent_notifications
    }