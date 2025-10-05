from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.views.decorators.csrf import csrf_exempt

from .views import UserRegistrationView, UserProfileView, UserUpdateView, UserDeleteView, UserChangePasswordView, UserVerifyEmail, UserRequestPasswordResetEmailView, UserVerifyPasswordResetEmailView, UserPasswordResetView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('me/', UserProfileView.as_view(), name='profile'),
    path('me/update/', UserUpdateView.as_view(), name='update'),
    path('me/delete/', UserDeleteView.as_view(), name='delete'),
    path('me/change-password/', UserChangePasswordView.as_view(), name='change-password'),
    
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('email-verify/<uidb64>/<token>/', UserVerifyEmail.as_view(), name='email-verify'),
    
    path('request-password-reset-email/', csrf_exempt(UserRequestPasswordResetEmailView.as_view()), name='request-password-reset-email'),
    path('password-reset-email-verify/<uidb64>/<token>/', UserVerifyPasswordResetEmailView.as_view(), name='verify-password-reset-email' ),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='password-reset'),
]
 