

from rest_framework.decorators import APIView , permission_classes , authentication_classes
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsUser

from product.models import Product
from .serializers import ShoppingCardSerializer , ShoppingListCardSerializer
from .models import ShoppingCard
from rest_framework import generics

class AddShoppingCardAPIView(APIView):
      permission_classes = [IsAuthenticated, IsUser]
      authentication_classes = [TokenAuthentication]

      def post(self, request, *args, **kwargs):

            try:
                  data = request.data  # {product_id: 3, quantity: 2}
                  serialzie_data = ShoppingCardSerializer(data=data)

                  product_id = data.get('product')
                  quantity = data.get('quantity')

                  product_exists = Product.objects.filter(id=product_id).exists()

                  if not product_exists:
                        return Response({'success': False, 'message': 'Product is not exists'}, status=status.HTTP_404_NOT_FOUND)

                  product = Product.objects.get(id=product_id)

                  if product.quantity < quantity:
                        return Response({'success': False, 'message': 'Product is out of stock'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                  total_price = product.price * quantity

                  new_shopping_card = {
                        'product': product,
                        'user': request.user,
                        'quantity': quantity,
                        'total_price': total_price
                  }

                  shopping_card = ShoppingCard(**new_shopping_card)

                  shopping_card.save()

                  return Response({'success': True, 'message': 'Product added to the shopping cart'}, status=status.HTTP_201_CREATED)

            except Product.DoesNotExist:
                  return Response({'success': False, 'message': 'Product is not exists'}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                  return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListShoppingCard(generics.ListAPIView):
      """ Shopping card retrive , update , delete only permissions for user """
      
      permission_classes = [IsAuthenticated , IsUser]
      authentication_classes = [TokenAuthentication]
      serializer_class = ShoppingListCardSerializer

      def get_queryset(self):
            return ShoppingCard.objects.filter(user = self.request.user.customuser)

class EditShoppingCard(generics.RetrieveUpdateDestroyAPIView):
      """ Shopping card retrive , update , delete only permissions for user """
      
      permission_classes = [IsAuthenticated , IsUser]
      authentication_classes = [TokenAuthentication]
      serializer_class = ShoppingCardSerializer
      
      def get_queryset(self):
                  return ShoppingCard.objects.filter(user = self.request.user.customuser)
      
      def update(self, request, *args, **kwargs):
            """ update the shopping card and update total_price based an quantity """

            # * get the shopping card instance
            instance = self.get_object()

            # * update the serializer
            serializer = self.get_serializer(instance , data = request.data , partial = True)

            if serializer.is_valid():
                  
                  # * get the quantity
                  new_quantity = serializer.validated_data['quantity']

                  # * get product
                  product = instance.product

                  # * calculate total price
                  new_total_price = product.price * new_quantity

                  # * update the instance
                  instance.quantity = new_quantity
                  instance.total_price = new_total_price
                  instance.save()

                  return Response({'success': True, 'message': 'Shopping card updated successfully'})

            else:
                  return Response({'success': False, 'message': serializer.errors} , status.HTTP_400_BAD_REQUEST)
