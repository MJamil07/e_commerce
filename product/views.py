
from .serializers import ProductSerializer
from .models import Product
from .permissions import IsSeller
from rest_framework.decorators import api_view , permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSeller
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from authenticator.models import CustomUser
from django.contrib.auth.models import User
from rest_framework import generics
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSeller])
@authentication_classes([TokenAuthentication])
def create_product(request, *args, **kwargs):
    """ Used to create a product only allowed for the seller """
    try:
        product_data = request.data
        custom_user = request.user.customuser  

        print(custom_user)

        serialize_product_data = ProductSerializer(data={'seller': custom_user.pk, **product_data})

        logger.info(f" create Product {request.user.customuser.role}  ")

        if serialize_product_data.is_valid():
            serialize_product_data.save()
            return Response({'success': True, 'data': serialize_product_data.validated_data}, status.HTTP_201_CREATED)

        return Response({'success': False, 'data': serialize_product_data.errors}, status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


    
class ListProductAPIView(generics.ListAPIView):
    """Read the product for both users and sellers"""
    serializer_class = ProductSerializer

    """ user read all products """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    """ seller reads only our product """
    def get_queryset(self):
        if self.request.user.customuser.role == 'seller':
            return Product.objects.filter(seller = self.request.user.customuser)
        return Product.objects.all()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product (only for sellers)"""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Product.objects.filter(seller = self.request.user.customuser)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def search_product(request):
    """Search for products based on name, category, and company."""
    
    try:
        name = request.query_params.get('name')
        category = request.query_params.get('category')
        company = request.query_params.get('company')

        filters = {}
        if name:
            filters['name__icontains'] = name
        if category:
            filters['category__icontains'] = category
        if company:
            filters['company__icontains'] = company

        filtered_products = Product.objects.filter(seller = self.request.user.customuser).filter(**filters)
        serialized_products = ProductSerializer(filtered_products, many=True)

        return Response({'success': True, 'data': serialized_products.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
