

from rest_framework.serializers import ModelSerializer
from .models import ShoppingCard

from product.models import Product
from django.contrib.auth.models import User

class ProductSerializer(ModelSerializer):

      class Meta:
            model = Product
            fields = ('name' , 'company' , 'category' , 'price' , 'rating')

class UserSerializer(ModelSerializer):

      class Meta:
            model = User
            fields = ('username' , )

class ShoppingListCardSerializer(ModelSerializer):

      product = ProductSerializer()
      user = UserSerializer()
      class Meta:
            model = ShoppingCard
            fields = '__all__'
            depth = 1

class ShoppingCardSerializer(ModelSerializer):

      class Meta:
            model = ShoppingCard
            fields = ('product' , 'quantity')
            