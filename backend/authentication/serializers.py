# myproject/myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser, Customer, Business

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_customer', 'is_business']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        if validated_data['is_customer']:
            Customer.objects.create(user=user)
        elif validated_data['is_business']:
            Business.objects.create(user=user)
        return user

