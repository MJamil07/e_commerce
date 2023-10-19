from rest_framework.decorators import api_view , APIView 
from .serializers import CustomUserSerializer , LoginSerializer , UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):
      permission_classes = [AllowAny]

      def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user_serializer = UserSerializer(data=data)

            if user_serializer.is_valid():
                new_user = User.objects.create(
                    username=data.get('username'),
                    email=data.get('email'),
                )

                new_user.set_password(data.get('password'))
                new_user.save()

                custom_user_serializer = CustomUserSerializer(data={'user': new_user.pk , **data})

                if custom_user_serializer.is_valid():
                    custom_user_serializer.save()

                    logger.info(f" {new_user.username} registered , role {data.get('role')} ")

                    return Response({'success': True, 'message': 'Successfully Registered'}, status=status.HTTP_201_CREATED)
                else:
                    new_user.delete()  # Rollback user creation if CustomUser creation fails
                    return Response({'success': False, 'message': custom_user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPIView(APIView):
      permission_classes = [AllowAny]

      def post(self , request , *args , **kwargs ):
            try:
                data = request.data
                serialize_data = LoginSerializer(data = data)
                print(data)
                if not serialize_data.is_valid():  
                    return Response({ 'success' : False , 'message' : serialize_data.error_messages} , status.HTTP_400_BAD_REQUEST)

                login_user = authenticate(request , username = data.get('username') , password = data.get('password'))
                print(login_user)
                # * check user register or not
                if not login_user :
                    return Response({ 'success' : False , 'message' : 'invalid credientials'} , status.HTTP_401_UNAUTHORIZED)
                
                # * create token first time login 
                token , created = Token.objects.get_or_create(user = login_user)
            
                logger.info(f" {login_user.get_username} is Login ")

                return Response({ 'success' : True , 'token' : str(token)} , status= status.HTTP_202_ACCEPTED)
        
            except Exception as e:
                  return Response({ 'success' : False , 'message' : str(e)} , status.HTTP_500_INTERNAL_SERVER_ERROR)


