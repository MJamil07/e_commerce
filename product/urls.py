from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
      path('create_product/' , views.create_product , name = 'create_product'),
      path('read_product/' , views.ListProductAPIView.as_view() , name = 'list_product'),
      path('edit_product/<int:pk>/' , views.ProductDetailAPIView.as_view() , name = 'edit_product'),
      path('search/' , views.search_product , name = 'search_product')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
