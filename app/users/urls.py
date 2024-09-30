from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="auth-register"),
    path("login/", TokenObtainPairView.as_view(), name="auth-token-obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
]
