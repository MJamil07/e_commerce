
from django.urls import path
from . import  views

urlpatterns = [
      path('create/' , views.CreateAPIView.as_view() , name = 'create_reviews'),
      path('list/' , views.ReviewList.as_view() , name = 'list_reviews'),
      path('edit/<int:pk>/' , views.ReviewRetriveUpdateDestroyAPIView.as_view() , name = 'edit_reviews'),
]     