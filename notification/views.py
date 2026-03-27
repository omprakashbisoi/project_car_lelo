from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from seller.models import CarDetail
from .models import Notification
from orders.models import Order


@login_required
def contact_request(request, car_id):
    car = get_object_or_404(CarDetail, id=car_id)

    if car.seller == request.user:
        return redirect('car_detail_view', car_id=car.id)

    already_exists = Notification.objects.filter(
        buyer=request.user,
        car=car,
        request_type='contact_request',
    ).exists()

    if not already_exists:
        Notification.objects.create(
            buyer=request.user,
            seller=car.seller,
            car=car,
            request_type='contact_request',
            status='pending',
            message=f"Interested in your {car.brand} {car.car_model}",
            visible_to='seller',
            is_read=False
        )

    return redirect('notification:base_notifications')


@login_required
def buy_request(request, car_id):
    car = get_object_or_404(CarDetail, id=car_id)

    if request.user == car.seller:
        return redirect('notification:base_notifications')

    already_exists = Notification.objects.filter(
        buyer=request.user,
        car=car,
        request_type='buy_request',
    ).exists()

    if not already_exists:
        Notification.objects.create(
            buyer=request.user,
            seller=car.seller,
            car=car,
            request_type='buy_request',
            status='pending',
            message=f"I want to buy your {car.brand} {car.car_model}",
            visible_to='seller',
            is_read=False
        )

    return redirect('notification:base_notifications')


@login_required
def handle_request_action(request, req_id, action):
    if request.method != 'POST':
        return redirect('notification:base_notifications')

    notif = get_object_or_404(Notification, id=req_id)

    if notif.seller != request.user:
        return redirect('notification:base_notifications')

    if notif.status != 'pending':
        return redirect('notification:base_notifications')

    with transaction.atomic():
        notif.status = 'accepted' if action == 'accept' else 'rejected'
        notif.is_read = True
        notif.action_taken_by = request.user
        notif.save()

        if action == 'accept':

            if notif.request_type == 'contact_request':
                Notification.objects.create(
                    buyer=notif.buyer,
                    seller=notif.seller,
                    car=notif.car,
                    request_type='contact_shared',
                    status=None,
                    message=f"Seller shared their contact: {notif.seller.email}",
                    parent_request=notif,
                    visible_to='buyer',
                    is_read=False
                )


            elif notif.request_type == 'buy_request':

                Order.objects.create(
                    user=notif.buyer,
                    car=notif.car,
                    car_name=f"{notif.car.brand} {notif.car.car_model}",
                    car_price=notif.car.price,
                    seller_name=notif.seller,
                    status='completed',
                )

                notif.car.is_sold = True
                notif.car.sold_at = timezone.now()
                notif.car.save(update_fields=['is_sold', 'sold_at'])

                Notification.objects.create(
                    buyer=notif.buyer,
                    seller=notif.seller,
                    car=notif.car,
                    request_type='buy_confirmation',
                    status=None,
                    message=f"Seller accepted your buy request for {notif.car.brand} {notif.car.car_model}",
                    parent_request=notif,
                    visible_to='buyer',
                    is_read=False
                )

                # Notify seller — sale recorded
                Notification.objects.create(
                    buyer=notif.buyer,
                    seller=notif.seller,
                    car=notif.car,
                    request_type='sell_confirmation',
                    status=None,
                    message=f"You confirmed the sale of {notif.car.brand} {notif.car.car_model} to {notif.buyer.username}",
                    parent_request=notif,
                    visible_to='seller',
                    is_read=False
                )


    return redirect('notification:base_notifications')


@login_required
def base_notifications(request):

    buyer_notifications = Notification.objects.filter(
        buyer=request.user,
        visible_to='buyer'
    ).order_by('-created_at')

    seller_notifications = Notification.objects.filter(
        seller=request.user,
        visible_to='seller'
    ).order_by('-created_at')

    buy_request_car_ids = set(
        Notification.objects.filter(
            buyer=request.user,
            request_type='buy_request'
        ).values_list('car_id', flat=True)
    )

    return render(request, 'notification/base_notifications.html', {
        'buyer_notifications': buyer_notifications,
        'seller_notifications': seller_notifications,
        'buy_request_car_ids': buy_request_car_ids,
    })


@login_required
def mark_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(
            Q(buyer=request.user, visible_to='buyer') |
            Q(seller=request.user, visible_to='seller') |
            Q(
                Q(buyer=request.user) | Q(seller=request.user),
                visible_to='both'
            ),
            is_read=False
        ).update(is_read=True)

    return redirect('notification:base_notifications')