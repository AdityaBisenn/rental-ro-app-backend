from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta

class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class CustomUser(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    is_customer = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Dealer(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='dealer_profile')
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Customer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    current_subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_customer')

    def __str__(self):
        return self.name

class Plan(TimeStampedModel):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(help_text='Duration in months')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    consumption_limit = models.IntegerField(help_text='In liters per month', null=True, blank=True)

    def __str__(self):
        return self.name

class Subscription(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='all_subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    consumption = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30 * self.plan.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.name} - {self.plan.name}'

class Device(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    installation_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='devices')
    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, related_name='devices')

    def __str__(self):
        return self.serial_number

class Chip(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chip_id = models.CharField(max_length=100, null=True)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, related_name='chips')
    version = models.CharField(max_length=50, null=True, blank=True)
    last_maintenance_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.chip_id
