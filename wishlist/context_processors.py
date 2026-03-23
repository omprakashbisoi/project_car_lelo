# wishlist/context_processors.py

from .models import Wishlist

def wishlist_data(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)

        wishlist_count = wishlist_items.count()
        recent_wishlist = wishlist_items.order_by('-created_at')[:5]

    else:
        wishlist_count = 0
        recent_wishlist = []

    return {
        'wishlist_count': wishlist_count,
        'recent_wishlist': recent_wishlist
    }