from django.urls import path
from . import views

urlpatterns = [
      path('create_shopping_card/' , views.AddShoppingCardAPIView.as_view() , name = 'create_shopping_card'),
      path('edit_shopping_card/<int:pk>/' , views.EditShoppingCard.as_view() , name = 'edit_shopping_card'),
      path('list_shopping_card/' , views.ListShoppingCard.as_view() , name = 'list_shopping_card'),

]