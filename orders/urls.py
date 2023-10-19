
from django.urls import path
from . import views

urlpatterns = [
      path('create/' , views.CreateOrdersAPIView.as_view() , name = 'create_order'),
      path('list/' , views.ListOrder.as_view() , name = 'list_order'),
      path('search/' , views.SearchProduct.as_view() , name = 'search_order'),
      path('cancel/' , views.cancel_order , name = 'cancel_order'),
]