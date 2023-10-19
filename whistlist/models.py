from django.db import models
from product.models import Product
from django.contrib.auth.models import User

# Create your models here.


class ShoppingCard(models.Model):
      """ Shopping card it stored favorite products """

      product = models.ForeignKey(Product , on_delete = models.CASCADE)
      user = models.ForeignKey(User , on_delete = models.CASCADE)
      total_price = models.IntegerField(default = 0)
      quantity = models.IntegerField(default = 1)

      def __str__(self):
            return f"[ product = {self.product} , user = {self.user} ]"