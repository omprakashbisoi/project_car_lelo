from django.db.models import Q
from .models import Notification


def notification_data(request):
    if not request.user.is_authenticated:
        return {
            'unread_count': 0,
            'recent_notifications': [],
        }

    # Buyer sees: responses they received (contact_shared, buy_confirmation)
    buyer_qs = Notification.objects.filter(
        buyer=request.user,
        visible_to='buyer'
    )

    # Seller sees: incoming pending requests only
    seller_qs = Notification.objects.filter(
        seller=request.user,
        visible_to='seller',
        status='pending'
    )

    all_notifications = (buyer_qs | seller_qs).distinct().order_by('-created_at')

    unread_count = all_notifications.filter(is_read=False).count()
    recent_notifications = all_notifications[:5]

    return {
        'unread_count': unread_count,
        'recent_notifications': recent_notifications,
    }