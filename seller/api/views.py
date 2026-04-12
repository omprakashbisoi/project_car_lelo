from location.utils import get_lat_lon
from seller.api.serializers import (
    ImageUploadSerializer,
    LocationSerializer,
    SellCarCreateSerializer,
    SellerDashboardCarSerializer,
    SellerDashboardImagesSerializer,
)
from seller.models import CarDetail, ImageStore
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action


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


class SellerDashboardCarListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerDashboardCarSerializer

    def get_queryset(self):
        return CarDetail.objects.filter(seller=self.request.user).select_related("car_location").order_by("-id")


class SellerDashboardCarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerDashboardCarSerializer
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return CarDetail.objects.filter(seller=self.request.user)

    def destroy(self, request, *args, **kwargs):
        car = self.get_object()
        car.images.all().delete()
        car.delete()
        return Response({"detail": "Car deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="toggle-availability")
    def toggle_availability(self, request, pk=None):
        car = self.get_object()
        car.is_available = not car.is_available
        car.save(update_fields=["is_available"])
        return Response(
            {"is_available": car.is_available, "detail": "Car availability updated successfully."},
            status=status.HTTP_200_OK,
        )

class SellerDashboardImageListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerDashboardImagesSerializer

    def get_queryset(self):
        return ImageStore.objects.filter(car__seller=self.request.user).select_related("car").order_by("-id")


class SellerDashboardImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerDashboardImagesSerializer
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return ImageStore.objects.filter(car__seller=self.request.user).select_related("car")

    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        image.car_image.delete(save=False)
        image.delete()
        return Response({"detail": "Image deleted successfully."}, status=status.HTTP_200_OK)
