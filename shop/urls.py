from django.urls import path
from .views import home, detail, shop

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('detail/', detail, name='detail'),
    path('shop/', shop, name='shop'),
    path('cart/', cart, name='cart'),

]