from django.shortcuts import render
from .models import ProductModel, CategoryModel

def home(request):
    return render(request, 'shop/home.html')


def detail(request):
    return render(request, 'shop/detail.html')

def shop(request):
    categories = CategoryModel.objects.all()
    products = ProductModel.objects.all()
    return render(request, 'shop/shop.html')
