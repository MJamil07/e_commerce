

from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

      class Meta :
            model = User;
            fields = ('username' , 'email' , 'password')

      def validate(self , data):
            
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')


            if not username:
                  raise serializers.ValidationError("username is required")

            if not password:
                  raise serializers.ValidationError("password is required")

            if not email:
                  raise serializers.ValidationError("email is required")

            if User.objects.filter(username__iexact=username).exists():
                  raise serializers.ValidationError(f"{username} already exists")


            if len(password) <= 8 :
                  raise serializers.ValidationError(f" Password is length must greater than 8")
            
            return data;

class CustomUserSerializer(serializers.ModelSerializer):


      class Meta :
            model = CustomUser;
            fields = "__all__"

      


class LoginSerializer(serializers.Serializer):

      username = serializers.CharField()
      password = serializers.CharField()

