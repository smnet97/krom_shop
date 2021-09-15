from django.shortcuts import render, redirect
from .models import CartModel, ProductModel, CategoryModel


def home(request):
    cotegory = CategoryModel.objects.all()
    return render(request, 'shop/home.html' , {'cotegory': cotegory})


def detail(request, pk):
    product = ProductModel.objects.get(id=pk)
    products = ProductModel.objects.filter(category=product.category)[:4]
    return render(request, 'shop/detail.html' , {'products':products , 'prod': product})

def shop(request):
    categories = CategoryModel.objects.all()
    products = ProductModel.objects.all()
    return render(request, 'shop/shop.html' , {'categories': categories, 'products': products})

def cart(request):
    carts = CartModel.objects.all()
    return render(request, 'shop/cart.html' , {'carts': carts})


def add_to_cart(request, pk):
    user = request.user
    product = ProductModel.objects.get(pk=pk)
    check_if_exsist = CartModel.objects.filter(product=product)
    if check_if_exsist:
        return redirect('shop:shop')
    created = CartModel.objects.create(user=user, product=product)
    if created:
        return redirect('shop:cart')


def delete_cart_item(request, pk):
    obj = CartModel.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:cart')


def clean_cart(request):
    pass

