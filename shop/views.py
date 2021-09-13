from django.shortcuts import render
from shop.models import CategoryModel,ProductModel

def home(request):
    cotegory = CategoryModel.objects.all()
    return render(request, 'shop/home.html' , {'cotegory': cotegory})


def detail(request):
    return render(request, 'shop/detail.html')

def shop(request):
    cotegory = CategoryModel.objects.all()
    product = ProductModel.objects.all()
    return render(request, 'shop/shop.html' , {'cotegory': cotegory, 'product': product})

def cart(request):
    cotegory = CategoryModel.objects.all()
    product = ProductModel.objects.all()
    return render(request, 'shop/cart.html' , {'cotegory': cotegory, 'product': product})
