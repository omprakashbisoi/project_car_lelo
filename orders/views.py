# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Order
# # Create your views here.

# @login_required
# def profile_view(request):
#     orders = Order.objects.filter(user=request.user)

#     context = {
#         "orders": orders,
#     }
#     return render(request, "profile.html", context)
