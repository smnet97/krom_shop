from django.shortcuts import render, redirect
from .models import CartModel, DeliveryCostModel, OrderModel, ProductModel, CategoryModel, ShippingAddressModel
from django.http import JsonResponse


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
    carts = CartModel.objects.all()
    delivery = DeliveryCostModel.objects.first()
    total = sum([i.get_total_price for i in carts])
    total_sum = delivery.delivery + total
    return render(request, 'shop/cart.html' , {'carts': carts, 'total':total, 'delivery':delivery, 'total_sum':total_sum })



def checkout(request):
    user = request.user
    carts = CartModel.objects.all()
    delivery = DeliveryCostModel.objects.first()
    total = sum([i.get_total_price for i in carts])
    print(request.POST)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        company = request.POST['company']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['checkout_city']
        region = request.POST['checkout_province']
        email = request.POST['email']
        check_address =  ShippingAddressModel.objects.filter(user=user)
        if not check_address:
            ShippingAddressModel.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone,
                                company=company, address1=address1, address2=address2, city=city, region=region, email=email)

        get_email = request.user.shippingaddressmodel.email
        print(get_email)

        if request.POST['radio'] == '1':
            payment_type = 1
        elif request.POST['radio'] == '2':
            payment_type = 2
        elif request.POST['radio'] == '3':
            payment_type = 3    
        
        done = OrderModel.objects.create(user=user, amount=total+delivery.delivery, phone=user.username, email=get_email, payment_type=payment_type,
                                        payment_status=1, delivery_status=1)
        if done:
            return redirect('shop:payment-check')
        
    return render(request, 'shop/checkout.html' , {'carts': carts, 'total':total+delivery.delivery})



def add_to_cart(request, pk):
    user = request.user
    product = ProductModel.objects.get(pk=pk)
    check_if_exsist = CartModel.objects.filter(product=product)
    if check_if_exsist:
        return redirect('shop:cart')
    created = CartModel.objects.create(user=user, product=product)
    if created:
        return redirect('shop:cart')


def delete_cart_item(request, pk):
    obj = CartModel.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:cart')


def clean_cart(request):
    obj = CartModel.objects.all()
    obj.delete()
    return redirect('shop:shop')


def  change_product_amount(request, pk):
    obj = CartModel.objects.get(pk=pk)
    obj.amount = request.GET.get('cart_amount')
    obj.save()
    return redirect('shop:cart')


def payment(request):
    return render(request, 'payment.html')

