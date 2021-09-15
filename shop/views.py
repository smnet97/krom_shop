from django.shortcuts import render
from shop.models import CategoryModel,ProductModel

def home(request):
    cotegory = CategoryModel.objects.all()
    return render(request, 'shop/home.html' , {'cotegory': cotegory})


def detail(request, pk):
    product = ProductModel.objects.get(id=pk)
    products = ProductModel.objects.filter(category=product.category)[:4]

    return render(request, 'shop/detail.html' , {'products':products , 'prod': product})

def shop(request):
    cotegory = CategoryModel.objects.all()
    product = ProductModel.objects.all()
    return render(request, 'shop/shop.html' , {'cotegory': cotegory, 'product': product})

def cart(request):
    cotegory = CategoryModel.objects.all()
    product = ProductModel.objects.all()
    return render(request, 'shop/cart.html' , {'cotegory': cotegory, 'product': product})

def checkout(request):
    return render(request, 'shop/checkout.html')
