from django.contrib import admin
from .models import CategoryModel, FavoritesModel, ProductModel, CartModel, ShippingAddressModel, DeliveryCostModel, OrderModel

admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(ShippingAddressModel)
admin.site.register(DeliveryCostModel)
admin.site.register(OrderModel)
admin.site.register(FavoritesModel)

