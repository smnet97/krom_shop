from rest_framework import serializers
from .models import CartModel, CategoryModel, FavoritesModel, ProductModel

class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class ProductModelSerialiser(serializers.ModelSerializer):
    category = CategorySerialiser(read_only=True)
    class Meta:
        model = ProductModel
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product = ProductModelSerialiser(read_only=True)
    class Meta:
        model = CartModel   
        fields = '__all__'      

class FavoritesSerializer(serializers.ModelSerializer):
    product = ProductModelSerialiser(read_only=True)
    class Meta:
        model = FavoritesModel
        fields = '__all__'  
