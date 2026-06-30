from django.urls import path
from .views import upload_locations, get_product_price

urlpatterns = [
    path("upload-locations/", upload_locations, name="upload_locations"),
    path('get-product-price/<int:pk>/', get_product_price),
]