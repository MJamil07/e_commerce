

from rest_framework import serializers
from .models import Review

from product.models import Product
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = Product
            fields = ('name' , 'company' , 'category' , 'price' , 'rating')

class UserSerializer(serializers.ModelSerializer):

      class Meta:
            model = User
            fields = ('username' , )

class ReviewListSerializer(serializers.ModelSerializer):
      product = ProductSerializer()
      user = UserSerializer()
      class Meta:
            model = Review
            fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):

      class Meta:
            model = Review
            fields = ['product' , 'comment' , 'rating']

      def validate(self , data):
            
            product_id = data.get('product')
            print('product' , product_id)
            if not Product.objects.filter(id = product_id.pk).exists():
                  raise serializers.ValidationError("Product not exists")

            return data
            