from django.db import models
from django.utils import timezone
# Create your models here.

# Product category Model
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Product supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length= 30)
    contact_info = models.TextField()

    def __str__(self):
        return self.name 
    

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    sku = models.CharField(unique=True, max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null= True, blank= True, on_delete = models.SET_NULL)
    supplier = models.ForeignKey(Supplier, null= True, blank= True, on_delete = models.SET_NULL)
    low_stock_threshold = models.PositiveIntegerField(default=5) # default threshold is set to 5 units

    def __str__(self):
        return self.name
    
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold


# Stock Logging Model
class StockLog(models.Model):
    ADDITION = 'ADDITION'
    REMOVAL = 'REMOVAL'

    REASON_CHOICES = [
        (ADDITION, 'Stock Addition'),
        (REMOVAL, 'Stock Removal'),
        ('SOLD OUT', 'Sold Out'),
        ('RETURN', 'Return'),
        ('DAMAGE', 'Damage'),
        ('DISPOSAL', 'Disposal'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    date_changed = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)

    def __str__(self):
        return f"{self.product} - {self.quantity_changed} units on {self.date_changed}"





