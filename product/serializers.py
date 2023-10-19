from rest_framework import serializers
from .models import Product
from reviews.models import Review
from reviews.serializers import ReviewListSerializer


class ProductSerializer(serializers.ModelSerializer):
    
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_comments(self, product):
        product_comments = Review.objects.filter(product=product)
        serialized_comments = [ReviewListSerializer(review).data for review in product_comments]
        return serialized_comments

