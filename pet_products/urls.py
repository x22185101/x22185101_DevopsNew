from django.urls import path
from . import views

app_name = 'pet_products'

urlpatterns = [
    path('pet_products/', views.product_list, name='pet_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),

 
]
