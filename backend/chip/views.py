from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.http import JsonResponse
import requests
from django.db import connection
import os
from authentication.models import CustomUser, Customer
from .utils import encrypt_json, decrypt_json
from django.views.decorators.csrf import csrf_exempt
import json

# Use a secure key with appropriate length for AES (16, 24, or 32 bytes)
key_24 = b"B\xb4'\xcf\x82?\r\x1b+\xc6\xa2\x83\x19\xca\xd5\x8f\xa7\x9d\xa4l\xed\xa9\x9f;"
# Hexadecimal representation for clarity: 123456789abcdef0123456789abcdef0

key = key_24  # Example key (must be kept secret and secure)

# Create your views here.

class ChipConnectionAPI(APIView):
    def post(self, request):
        try:
            auth_header = request.headers.get('ChipVerification')

            # Check if auth_header is present and correctly formatted
            if not auth_header or not auth_header.startswith('Chip '):
                return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

            token = auth_header.split(' ')[1]
            
            # Decrypt the token
            try:
                decrypted_data = decrypt_json(token, key)
            except (ValueError, KeyError) as e:
                return JsonResponse({'error': 'Invalid token or decryption failed'}, status=400)

            chip_id = decrypted_data.get('chip_id')
            mac_address = decrypted_data.get('mac_address')

            if not chip_id or not mac_address:
                return JsonResponse({'error': 'Invalid token data'}, status=400)

            # Access additional data sent in the request body
            ltrs_used = request.data.get('ltrs_used')

            # Process the chip_id, mac_address, and ltrs_used as needed
            response_data = {
                'message': 'Token received and decrypted successfully',
                'chip_id': chip_id,
                'mac_address': mac_address,
                'ltrs_used': ltrs_used,
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GetChipTokenAPI(APIView):
    def post(self, request):
        try:
            # Extract mac_address and chip_id from the request data
            mac_address = request.data.get('mac_address')
            chip_id = request.data.get('chip_id')
            
            if not mac_address or not chip_id:
                return Response(
                    {"error": "mac_address and chip_id are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the JSON payload
            data = {
                "chip_id": chip_id,
                "mac_address": mac_address
            }
            
            # Encrypt the JSON payload
            encrypted_data = encrypt_json(data, key)
            
            # Return the encrypted data
            return Response({"encrypted_data": encrypted_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyChipTokenAPI(APIView):
    def post(self, request):
        try:
            encrypted_data = request.data.get('encrypted_data')
            
            if not encrypted_data:
                return Response(
                    {"error": "encrypted_data is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                decrypted_data = decrypt_json(encrypted_data, key)
            except (ValueError, KeyError) as e:
                return Response(
                    {"error": "Invalid token or decryption failed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            mac_address = decrypted_data.get('mac_address')
            chip_id = decrypted_data.get('chip_id')
            
            if not mac_address or not chip_id:
                return Response(
                    {"error": "Invalid token data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(decrypted_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

