from django.contrib import admin
from .models import CategoryModel, ProductModel, CartModel

admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(CartModel)

