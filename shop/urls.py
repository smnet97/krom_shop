from os import name
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

    path('', views.home, name='home'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('delete_cart_item/<int:pk>/', views.delete_cart_item, name='delete-cart-item'),
    path('clean_cart', views.clean_cart, name='clean-cart'),
    path('change_product_amount/<int:pk>/', views.change_product_amount, name='change-product-amount'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:pk>/', views.add_to_favorites, name='favorites'),
    path('delete_favorite_item/<int:pk>/', views.delete_favorite_item, name='delete-favorite-item'),
    path('clean_favorites/', views.clean_favorites, name='clean-favorites'),
    path('order_detail/<int:pk>/', views.order_detail, name='order-detail'),
    path('payment/', views.payment, name='payment-check'),
    

]