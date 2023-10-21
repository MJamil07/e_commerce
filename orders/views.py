

from rest_framework.decorators import APIView , api_view , permission_classes , authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from .serializers import OrderSerializer
from .permissions import IsUser
from rest_framework import generics
from .models import Order
from rest_framework.serializers import ModelSerializer

class CreateOrdersAPIView(APIView):

      permission_classes = [IsAuthenticated , IsUser]
      authentication_classes = [TokenAuthentication]

      def post(self , request , *args , **kwargs):
            """ create orders only allowed for user """

            try:
                  order_data = request.data;
                  product_id = order_data.get('product')
                  quantity = order_data.get('quantity')

                  # * check if product exists are not
                  if not Product.objects.filter(id = product_id).exists():
                        return Response({'success' : False , 'message' : 'Product not exist' } , status.HTTP_404_NOT_FOUND)

                  if 'status' in order_data:
                        order_data['status'] = 'process'

                  current_product = Product.objects.get(id = product_id)

                  if current_product.quantity < quantity:
                        return Response({'success' : False , 'message' : f'Product Out Of Stock available quantity {current_product.quantity}'} , status.HTTP_400_BAD_REQUEST)

                  serialized_data = OrderSerializer(data = {'user' : request.user.pk , **order_data})

                  # * validate the data
                  if not serialized_data.is_valid():
                        return Response({'success' : False , 'message' : serialized_data.errors } , status.HTTP_400_BAD_REQUEST)

                  serialized_data.save()

                  return Response({'success' : True , 'message' : 'Order Successfull'} , status.HTTP_200_OK)
            
            except Exception as e:
                  return Response({'success' : False , 'message' : str(e)} , status.HTTP_500_INTERNAL_SERVER_ERROR)



class ListOrder(generics.ListAPIView):

      permission_classes = [IsAuthenticated]
      authentication_classes = [TokenAuthentication]

      serializer_class = OrderSerializer
      queryset = Order.objects.all()

      def list(self , request , *args , **kwargs):
            try:
                  if request.user.customuser.role == 'user':
                        ListOrder.queryset = Order.objects.filter(user = request.user)

                  elif request.user.customuser.role == 'seller':

                        # * get all products current seller product
                        current_seller_product = Product.objects.filter(seller = request.user.customuser)

                        # * get which orders hold by current seller product
                        orders = Order.objects.filter(product__in = current_seller_product)
                        
                        ListOrder.queryset = orders

                  return super().list(request , args , kwargs)

            except Exception as e:
                  return Response({'success' : False , 'message' : str(e)} , status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchProduct(APIView):

      permission_classes = [IsAuthenticated]
      authentication_classes = [TokenAuthentication]

      def get(self , request , *args , **kwargs):
            
            try:
                  options = ['process' , 'shipping' , 'delivered' , 'cancel']
                  option = request.GET.get('option')

                  if option in options:
                        if request.user.customuser.role == 'user':
                              oreders = Order.objects.filter(user = request.user).filter(status__icontains = option)
                              serialized_data = OrderSerializer(data = oreders , many = True)
                              return Response(serialized_data.data)
                        else:
                              current_seller_product = Product.objects.filter(seller = request.user.customuser)
                              orders = Order.objects.filter(product__in = current_seller_product).filter(status__icontains = option)
                              serialized_data = OrderSerializer(data = oreders , many = True)
                              return Response(serialized_data.data)
                  
                  return Response({'success' : False , 'message' : f'Your {option} status is not found'} , status.HTTP_204_NO_CONTENT)

            except Exception as e:
                  return Response({'success' : False , 'message' : str(e)} , status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsUser])
@authentication_classes([TokenAuthentication])
def cancel_order(request, order_id, *args, **kwargs):
      try:
            cancel_order = Order.objects.filter(user=request.user, id=order_id).first()
            if cancel_order:
                  cancel_order.status = 'cancel'
                  cancel_order.save()
                  return Response({'success': True, 'message': 'Order Cancelled Successfully'}, status=status.HTTP_200_OK)

            return Response({'success': False, 'message': 'Your Order Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
      
      except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

