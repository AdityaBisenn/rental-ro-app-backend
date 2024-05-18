# myproject/myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.http import JsonResponse
import requests
from django.db import connection
import os
from authentication.models import CustomUser, Customer, Business
from google.oauth2 import id_token
from google.auth.transport import requests


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serialized_user = UserSerializer(user).data  # Serialize user data
            return Response({
                'user': serialized_user,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

# Helper function to generate JWT token


def generate_jwt_token(user):
    # Generate refresh token without expiration time
    refresh = RefreshToken.for_user(user)

    # Generate access token without expiration time
    access = AccessToken.for_user(user)

    # Set expiration time for both tokens to a distant future timestamp
    # For example, setting expiration time to 100 years from now
    refresh['exp'] = datetime.now() + timedelta(days=36500)
    access['exp'] = datetime.now() + timedelta(days=36500)

    return {
        'refresh': str(refresh),
        'access': str(access),
    }


class GoogleTokenExchangeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        # Extract the Google access token from the request data
        token = request.data.get('token')

        # Verify Google access token
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        userEmail = idinfo['email']

        if userEmail:
            # Try to retrieve the user based on email
            user, created = CustomUser.objects.get_or_create(
                email=userEmail, username=userEmail)

            if created:
                user.is_customer = True
                Customer.objects.create(user=user)
                user.save()

            # Authenticate the user using the custom authentication backend
            user = authenticate(request, email=userEmail)

            if user:
                # If user is authenticated, log them in
                login(request, user)

                # Generate JWT tokens with non-expiring time
                jwt_tokens = generate_jwt_token(user)

                # Serialize user data
                serialized_user = UserSerializer(user).data
                print(serialized_user)

                return Response({
                    'user': serialized_user,
                    **jwt_tokens,
                    'message': 'User authenticated successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to authenticate user'}, status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse({'message': 'Token verified successfully'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_route(request):
    return Response({'message': 'This is a protected route'}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Test(APIView):
    def get(self, request):
        # Check PostgreSQL connection
        try:
            # Use a simple query to test the connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row:
                    connected = True
                else:
                    connected = False
        except Exception as e:
            connected = False

        if connected:
            message = 'PostgreSQL server is connected.'
        else:
            message = 'Failed to connect to PostgreSQL server.'

        return Response({'message': message})
