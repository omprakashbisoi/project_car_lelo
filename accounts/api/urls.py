from django.urls import path

from accounts.api.views import (
    CompleteRegistrationAPIView,
    CurrentUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    PasswordResetVerifyOTPAPIView,
    RegisterEmailAPIView,
    VerifyEmailOTPAPIView,
)

urlpatterns = [
    path("register/", RegisterEmailAPIView.as_view(), name="account_api_register"),
    path("register/verify-otp/", VerifyEmailOTPAPIView.as_view(), name="account_api_verify_otp"),
    path("register/complete/", CompleteRegistrationAPIView.as_view(), name="account_api_complete_registration"),
    path("login/", LoginAPIView.as_view(), name="account_api_login"),
    path("logout/", LogoutAPIView.as_view(), name="account_api_logout"),
    path("me/", CurrentUserAPIView.as_view(), name="account_api_me"),
    path("password/reset/", PasswordResetRequestAPIView.as_view(), name="account_api_password_reset"),
    path("password/verify-otp/", PasswordResetVerifyOTPAPIView.as_view(), name="account_api_password_verify_otp"),
    path("password/confirm/", PasswordResetConfirmAPIView.as_view(), name="account_api_password_confirm"),
]
