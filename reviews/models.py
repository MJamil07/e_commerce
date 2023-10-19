from django.db import models
from django.contrib.auth.models import User
from product.models import Product



class Review(models.Model):

      user = models.ForeignKey(User , on_delete = models.CASCADE)
      product = models.ForeignKey(Product , on_delete = models.CASCADE)
      comment = models.TextField()
      rating = models.IntegerField()

      def __str__(self):
            return f" [ comment = {self.comment} ] , user = {self.user} , product = {self.product} ]"