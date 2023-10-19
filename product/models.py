from django.db import models
from django.contrib.auth.models import User
from authenticator.models import CustomUser

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home'),
        ('sports', 'Sports'),
    )

    name = models.CharField(max_length=30)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    company = models.CharField(max_length=50)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    is_assured = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    offer = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(CustomUser , on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'Comment on {self.product.name} by {self.user.username}'
