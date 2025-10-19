from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


User = get_user_model()

from eden_backend.utils import Util
from .tokens import account_activation_token, password_reset_token
from .serializers import UserRegistrationSerializer, UserSerializer, UserChangePasswordSerializer, UserRequestPasswordResetEmailSerializer,          UserPasswordResetSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token = account_activation_token.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify', kwargs={'uidb64': uidb64, 'token': token})
        abslink = f"http://{current_site}{relativeLink}"
        email_body = f"Hi {user.first_name}, \n Use the link below to verify your email \n {abslink}"
        email_data = {
            'to_email':user.email,
            'email_subject': "Verify your email - EDen",
            'email_body': email_body,
        }
        
        Util.send_email(email_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserVerifyEmail(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        def update(self, request, *args, **kwargs):
            user = request.user
            if not user.check_password(request.data['current_password']):
                return Response({'current_password':'Invalid current password.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(request.data['new_password'])
            user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        
class UserRequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = UserRequestPasswordResetEmailSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        
        if user:
            token = password_reset_token.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            
            current_site = get_current_site(request).domain
            relative_link = reverse('verify-password-reset-token', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{current_site}{relative_link}"
            
            email_body = f"Hello, \nUse the link below to reset your rentiq password: \n{abslink} \nIgnore if you haven't requested a password reset."
            
            email_data = {
                'to_email': user.email,
                'email_subject': "Password Reset - EDen",
                'email_body': email_body,
            }
            
            Util.send_mail(email_data)
            
        return Response({'success': 'If an account with the email exists, you will receive an email.'}, status=status.HTTP_200_OK)
    
    
class UserVerifyPasswordResetEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self,request, uidb64, token):
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not password_reset_token.check_token(user, token):
                return Response({'error': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'success':True, 'message':'Credentials Valid'}, status=status.HTTP_200_OK)
        
        except (User.DoesNotExist):
            return Response({'error': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserPasswordResetView(generics.GenericAPIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = [AllowAny]
    
    def patch(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist):
            return Response({'Error': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password_reset_token.check_token(user, token):
            return Response({'Error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
    
    
class UserDeleteView(generics.DestroyAPIView):
    
    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user=request.user
        password = request.data.get['password']
        
        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_403_FORBIDDEN)
        
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        