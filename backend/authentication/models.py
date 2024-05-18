from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import FashionProduct, Cart

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    saved_products = models.ManyToManyField(FashionProduct, related_name='saved_products', blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username + ' (Customer)'

class Business(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    # Add any additional fields specific to businesses

    def __str__(self):
        return self.user.username + ' (Business)'
