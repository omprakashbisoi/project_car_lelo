from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import (
    CompleteRegistrationSerializer,
    EmailSerializer,
    LoginSerializer,
    OTPSerializer,
    PasswordSerializer,
    UserSerializer,
)
from accounts.models import CustomUser, EmailOTP, PasswordResetOTP
from accounts.utils import generate_otp


class RegisterEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        if CustomUser.objects.filter(email=email).exists():
            return Response({"email": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        otp_obj = EmailOTP.objects.filter(email=email).first()

        if otp_obj:
            if otp_obj.last_sent_at and now - otp_obj.last_sent_at > timedelta(hours=12):
                otp_obj.resend_count = 0
            if otp_obj.resend_count >= 3:
                return Response(
                    {"detail": "Resend limit reached. Try again after 12 hours."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
        else:
            otp_obj = EmailOTP(email=email, resend_count=0)

        otp = generate_otp()
        otp_obj.otp = otp
        otp_obj.expiry_time = now + timedelta(minutes=5)
        otp_obj.resend_count += 1
        otp_obj.last_sent_at = now
        otp_obj.is_verified = False
        otp_obj.save()

        send_mail(
            subject="Your OTP code",
            message=f"Your OTP is {otp}. It is valid for 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        request.session["pending_email"] = email
        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)


class VerifyEmailOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.session.get("pending_email") or request.data.get("email")
        if not email:
            return Response({"detail": "Register an email first."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_obj = EmailOTP.objects.filter(email=email).first()
        if not otp_obj:
            return Response({"detail": "Request a new OTP."}, status=status.HTTP_400_BAD_REQUEST)
        if otp_obj.is_expired():
            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
        if otp_obj.otp != serializer.validated_data["otp"]:
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_verified = True
        otp_obj.save(update_fields=["is_verified"])
        request.session["verified_email"] = email
        request.session.pop("pending_email", None)

        return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)


class CompleteRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        verified_email = request.session.get("verified_email") or request.data.get("email")
        if not verified_email:
            return Response({"detail": "Verify your email first."}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj = EmailOTP.objects.filter(email=verified_email, is_verified=True).first()
        if not otp_obj:
            return Response({"detail": "Verify your email first."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompleteRegistrationSerializer(data=request.data, context={"email": verified_email})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        request.session.pop("verified_email", None)
        send_mail(
            subject="Welcome to Car Lelo",
            message=f"Hi {user.first_name}, your account is ready!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        login(request, user)

        return Response(UserSerializer(user, context={"request": request}).data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(UserSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data, status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "If the email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

        now = timezone.now()
        otp_obj = PasswordResetOTP.objects.filter(user=user).first()
        if otp_obj:
            if otp_obj.last_sent_at and now - otp_obj.last_sent_at > timedelta(hours=12):
                otp_obj.resend_count = 0
            if otp_obj.resend_count >= 3:
                return Response(
                    {"detail": "Too many attempts. Try again after 12 hours."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
        else:
            otp_obj = PasswordResetOTP(user=user, resend_count=0)

        otp = generate_otp()
        otp_obj.otp = otp
        otp_obj.expiry_time = now + timedelta(minutes=3)
        otp_obj.resend_count += 1
        otp_obj.last_sent_at = now
        otp_obj.is_verified = False
        otp_obj.save()

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}. Valid for 3 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        request.session["reset_user"] = user.id

        return Response({"detail": "If the email exists, an OTP has been sent."}, status=status.HTTP_200_OK)


class PasswordResetVerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.session.get("reset_user")
        if not user_id:
            return Response({"detail": "Request a password reset first."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_obj = PasswordResetOTP.objects.filter(user_id=user_id).first()

        if not otp_obj:
            return Response({"detail": "Request a new OTP."}, status=status.HTTP_400_BAD_REQUEST)
        if otp_obj.is_expired():
            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
        if otp_obj.otp != serializer.validated_data["otp"]:
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_verified = True
        otp_obj.save(update_fields=["is_verified"])
        request.session["otp_verified"] = True
        return Response({"detail": "OTP verified successfully."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.session.get("reset_user")
        if not user_id or not request.session.get("otp_verified"):
            return Response({"detail": "Verify your OTP first."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordSerializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])

        request.session.pop("reset_user", None)
        request.session.pop("otp_verified", None)
        send_mail(
            subject="Password Changed",
            message="Your password was changed successfully.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
