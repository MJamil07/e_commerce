from django.db import models
from product.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    
    ORDER_STATUS = (
        ('delivered', 'Delivered'),
        ('process', 'Process'),
        ('shipping', 'Shipping'),
        ('cancel', 'Cancel'),
    )

    PAYMENT_OPTION = (
        ('cash', 'CASH ON PRICE'),
        ('upi', 'UPI SYSTEM'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='process')
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTION, default='cash')

    def __str__(self):
        return f"[ user = {self.user} , price = {self.total_price} ]"