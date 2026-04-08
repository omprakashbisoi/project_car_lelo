from location.utils import get_lat_lon
from seller.api.serializers import (
    ImageUploadSerializer,
    LocationSerializer,
    SellCarCreateSerializer,
)
from seller.models import CarDetail
from rest_framework import generics, status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class SellCarDetailAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellCarCreateSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        self.request.user.role = 'seller'
        self.request.user.save(update_fields=["role"])


class LocationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        try:
            car = CarDetail.objects.get(id=car_id, seller=request.user)
        except CarDetail.DoesNotExist:
            return Response({"detail": "Car not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        location = serializer.save(location_type="car")
        car.car_location = location
        car.save(update_fields=["car_location"])

        if location.city and location.state and location.pin:
            try:
                lat, lon = get_lat_lon(location.city, location.state, location.pin)
                if lat is not None and lon is not None:
                    location.latitude = lat
                    location.longitude = lon
                    location.save(update_fields=["latitude", "longitude"])
            except Exception:
                return Response(
                    {"detail": "Something went wrong while loading location. Please check and try again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(LocationSerializer(location).data, status=status.HTTP_201_CREATED)
    
class ImageUploadAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageUploadSerializer
    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get("car_id")

        try:
            car = CarDetail.objects.get(id=car_id, seller=request.user)
        except CarDetail.DoesNotExist:
            return Response({"detail": "Car not found."}, status=status.HTTP_404_NOT_FOUND)

        image_serializer = self.get_serializer(data=request.data)
        image_serializer.is_valid(raise_exception=True)
        exist_image = car.images.filter(img_type=request.data.get("img_type")).first()
        if exist_image:
            exist_image.car_image.delete(save=False)
            exist_image.delete() 
        image_serializer.save(car=car)

        return Response(image_serializer.data, status=status.HTTP_201_CREATED)
