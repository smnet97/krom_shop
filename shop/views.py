from django.shortcuts import render
from .models import ProductModel, CategoryModel


def home(request):
    cotegory = CategoryModel.objects.all()
    return render(request, 'shop/home.html' , {'cotegory': cotegory})


def detail(request):
    return render(request, 'shop/detail.html')

def shop(request):

    categories = CategoryModel.objects.all()
    products = ProductModel.objects.all()
    return render(request, 'shop/shop.html' , {'categories': categories, 'products': products})

def cart(request):
    cotegory = CategoryModel.objects.all()
    product = ProductModel.objects.all()
    return render(request, 'shop/cart.html' , {'cotegory': cotegory, 'product': product})

