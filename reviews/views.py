from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReviewSerializer , ReviewListSerializer
from .models import Review
from orders.models import Order
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUser
from product.models import Product
from rest_framework import generics

class CreateAPIView(APIView):

      permission_classes = [IsAuthenticated, IsUser]
      authentication_classes = [TokenAuthentication]

      def post(self, request, *args, **kwargs):

            try:
                  review_data = request.data
                  serializer_data = ReviewSerializer(data = review_data)
                  print('review ' , review_data)

                  if not serializer_data.is_valid():
                        return Response({'success': False, 'message': serializer_data.errors}, status.HTTP_400_BAD_REQUEST)

                  print('review ' , review_data)

                  current_user = request.user
                  product_id = review_data.get('product')
                  product = Product.objects.get(id = product_id)

                  #  * check if user order this product or not
                  if not Order.objects.filter(user=current_user, product=product.pk).exists():
                        return Response({'success': False, 'message': 'You did not order this product'}, status.HTTP_401_UNAUTHORIZED)
                  print('review ' , review_data)

                  new_review = Review.objects.create(user = request.user , product = product , comment = review_data.get('comment') , rating = review_data.get('rating'))
                  return Response({'success': True, 'message': 'Your review has been added'}, status.HTTP_200_OK)

            except Exception as e:
                  return Response({'success': False, 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewList(generics.ListAPIView):
      
      permission_classes = [IsUser , IsAuthenticated]
      authentication_classes = [TokenAuthentication]
      serializer_class = ReviewListSerializer
      
      def get_queryset(self):
            return Review.objects.filter(user = self.request.user)

class ReviewRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

      permission_classes = [IsUser , IsAuthenticated]
      authentication_classes = [TokenAuthentication]
      serializer_class = ReviewSerializer
      
      def get_queryset(self):
            return Review.objects.filter(user = self.request.user)

      def update(self , request , *args , **kwargs):

            instance = self.get_object()

            if not Order.objects.filter(user = request.user , product = instance.product).exists():
                  return Response({'success': False, 'message': 'You did not order this product'}, status.HTTP_401_UNAUTHORIZED)

            return super().update(request , args , kwargs)