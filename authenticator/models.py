from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    """This authentication model applicable for user and seller"""
    
    ROLE_CHOICES = (
        ('user', 'USER'),
        ('seller', 'SELLER'),
    )

    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, null=False, blank=False)  
    home_address = models.CharField(max_length=20, null=False, blank=False)
    street = models.CharField(max_length=20, null=False, blank=False)
    pincode = models.CharField(max_length=10, null=False, blank=False)

    # * mapping by user
    user = models.OneToOneField(User , on_delete = models.CASCADE)

    def __str__(self):
        return f'[role = {self.role}]'

  