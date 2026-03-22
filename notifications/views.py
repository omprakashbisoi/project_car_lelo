from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from seller.models import CarDetail
from .models import ContactRequest


@login_required
def send_request(request, car_id):
    car = get_object_or_404(CarDetail, id=car_id)

    # ❌ Prevent seller from contacting own car
    if car.seller == request.user:
        return redirect('car_detail_view', car_id=car.id)

    # ✅ Prevent duplicate request
    already_sent = ContactRequest.objects.filter(
        buyer=request.user,
        car=car
    ).exists()

    if not already_sent:
        ContactRequest.objects.create(
            buyer=request.user,
            seller=car.seller,
            car=car,
            message=f"Hey, I am interested in your car {car.brand} {car.car_model}"
        )

    return redirect('car_detail_view', car_id=car.id)


@login_required
def seller_notification(request):
    seller_requests = ContactRequest.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    return render(request, 'notifications/seller_notifications.html', {
        "seller_requests": seller_requests
    })


@login_required
def buyer_notification(request):
    buyer_requests = ContactRequest.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    return render(request, 'notifications/buyer_notifications.html', {
        "buyer_requests": buyer_requests
    })


@login_required
def accept_request(request, req_id):
    req = get_object_or_404(ContactRequest, id=req_id)

    # 🔐 Only seller can accept
    if req.seller != request.user:
        return redirect('notifications:base_notifications')

    req.status = "accepted"
    req.is_read = True
    req.save()

    return redirect('notifications:seller_notification')


@login_required
def reject_request(request, req_id):
    req = get_object_or_404(ContactRequest, id=req_id)

    # 🔐 Only seller can reject
    if req.seller != request.user:
        return redirect('notifications:base_notifications')

    req.status = "rejected"
    req.is_read = True
    req.save()

    return redirect('notifications:seller_notification')


@login_required
def base_notifications(request):
    buyer_requests = ContactRequest.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    seller_requests = ContactRequest.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    return render(request, 'notifications/base_notifications.html', {
        'buyer_requests': buyer_requests,
        'seller_requests': seller_requests,
    })


@login_required
def mark_as_read(request):
    ContactRequest.objects.filter(
        seller=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({'status': 'ok'})