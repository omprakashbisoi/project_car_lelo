from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from seller.models import CarDetail
from wishlist.models import Wishlist

class WishlistApiView(APIView):
    permission_classes = [AllowAny]

    def post(self,request,car_id):
        if not request.user.is_authenticated:
            return Response({"detail":"For wishlist you have to login fast"},status=status.HTTP_401_UNAUTHORIZED)

        car = get_object_or_404(CarDetail, id=car_id)
        wishlist,create = Wishlist.objects.get_or_create(user=request.user,car=car)

        if create:
            return Response({"wished":True,"detail":"Car is added in your wishlist"},status=status.HTTP_200_OK)

        wishlist.delete()
        return Response({"wished":False,"detail":"Car is removed from your wishlist"},status=status.HTTP_200_OK)
