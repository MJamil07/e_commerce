
from rest_framework.serializers import ModelSerializer
from .models import Order

class OrderSerializer(ModelSerializer):
      
      class Meta:
            
            model = Order
            exclude = ['user']
            fields = '__all__'
      