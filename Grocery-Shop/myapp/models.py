import uuid
from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

def custom_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}.{ext}"
    return os.path.join('products/', new_filename)
    
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    stock = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to=custom_upload_path) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField()
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def cart_price(self):
       return sum(item.total_price for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def add_item(self):
        self.quantity += 1
        self.save()

    def remove_item(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
        else:
            self.delete()

    def delete_product(self):
        self.delete()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    