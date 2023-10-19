from rest_framework import permissions
from authenticator.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class IsUser(permissions.BasePermission):

      def has_permission(self , request , view):

            print(request.user)
            print(request.user.is_authenticated)

            if request.user and request.user.is_authenticated:
                  custom_user = CustomUser.objects.get(user = request.user.pk)
                  return custom_user.role == 'user'

            return False



