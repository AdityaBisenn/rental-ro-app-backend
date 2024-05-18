from django.db import models
# from authentication.models import Customer


class FashionProduct(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.CharField()
    images = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    colour = models.CharField(max_length=100, null=True, blank=True)
    sizes = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    num_reviews = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=100, null=True, blank=True)
    category_details = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_items = models.ManyToManyField('CartItem', related_name='cart_items', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user.username}'s cart"

class CartItem(models.Model):
    product = models.ForeignKey(FashionProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cart.customer.user.username}'s cart item"