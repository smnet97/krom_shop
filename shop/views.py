from inspect import isframe
from django.shortcuts import render, redirect
from .models import CartModel, DeliveryCostModel, FavoritesModel, OrderModel, ProductModel, CategoryModel, ShippingAddressModel
from django.http import JsonResponse, HttpResponse
from .serializers import CartSerializer, FavoritesSerializer
from django.contrib import messages



def home(request):
    """ 
    This function returns shops home page  
    """
    cotegory = CategoryModel.objects.all()
    return render(request, 'shop/home.html' , {'cotegory': cotegory})



def detail(request):
    return render(request, 'shop/detail.html')



def shop(request):
    """ 
    This function returns all items from the CategoryModel and ProductModel 
    """
    categories = CategoryModel.objects.all()
    products = ProductModel.objects.all()
    return render(request, 'shop/shop.html' , {'categories': categories, 'products': products})



def cart(request):
    """ 
    This function returns users cart detail  
    """
    delivery = DeliveryCostModel.objects.first()
    if request.user.is_authenticated:
        carts = CartModel.objects.filter(user=request.user)
        total = sum([i.get_total_price for i in carts])
        total_sum = delivery.delivery + total
        return render(request, 'shop/cart.html' , {'carts': carts, 'total':total, 'delivery':delivery, 'total_sum':total_sum })
        
    return render(request, 'shop/cart.html')



def checkout(request):
    """ 
    This function saves users shipping address information and also creates order 
    """
    if request.user.is_authenticated:
        user = request.user
        carts = CartModel.objects.filter(user=user)
        delivery = DeliveryCostModel.objects.first()
        total = sum([i.get_total_price for i in carts])

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
            address =  ShippingAddressModel.objects.filter(user=user)
            if not address:
                ShippingAddressModel.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone,
                                    company=company, address1=address1, address2=address2, city=city, region=region, email=email)
            else:
                current_address = address.first()
                current_address.user = user
                current_address.first_name = first_name
                current_address.last_name = last_name
                current_address.phone = phone
                current_address.company = company
                current_address.address1 = address1
                current_address.address2 = address2
                current_address.city = city
                current_address.region = region
                current_address.email = email
                current_address.save()

            get_email = request.user.shippingaddressmodel.email

            if request.POST['radio'] == '1':
                payment_type = 1
            elif request.POST['radio'] == '2':
                payment_type = 2
            elif request.POST['radio'] == '3':
                payment_type = 3    
            
            done = OrderModel.objects.create(user=user, amount=total+delivery.delivery, phone=user.username, email=get_email, payment_type=payment_type,
                                            payment_status=1, delivery_status=1)
            if done.payment_type == 1:
                return redirect('user:dashboard')
            elif done.payment_type == 2:
                return redirect('shop:payment-check')
        
        return render(request, 'shop/checkout.html' , {'carts': carts, 'total':total+delivery.delivery})

    else:
        return redirect('user:login')



def add_to_cart(request, pk):
    """ 
    This function adds a product item to the CartModel in both cases for autheticated user and for not  
    """
    product = ProductModel.objects.get(pk=pk)
    if request.user.is_authenticated:
        check_user_cart = CartModel.objects.filter(user=request.user, product=product)
        if check_user_cart:
            return redirect('shop:cart')
        CartModel.objects.create(user=request.user, product=product)
        return redirect('shop:cart')
    
    request.GET.get('cart_amount')

    obj = {
        "user" : None,
        "product" : product,
        "amount" : 1
    }
    serializer = CartSerializer(obj, many=False)
    data = serializer.data
    cart = request.session.get('cart', [])
    request.session['delivery'] = DeliveryCostModel.objects.first().delivery
    
    # request.session['total_sum'] = 0
    if data in cart:
        request.session['cart'] = cart
        return redirect('shop:cart')
    cart.append(data)
    request.session['cart'] = cart

    total = []
    for i in cart:
        total.append(i['product']['price'] * int(i['amount']))
    request.session['total'] = sum(total)
    total_sum = sum(total)+request.session['delivery']
    request.session['total_sum'] = total_sum 
    request.session.modified = True

    return redirect('shop:cart')


def delete_cart_item(request, pk):
    """ 
    This function deletes an item from the CartModel 
    """
    if request.user.is_authenticated:
        obj = CartModel.objects.get(pk=pk)
        obj.delete()
    
    else:
        for i in range(len(request.session['cart'])):
            if request.session['cart'][i]['product']['id'] == pk:
                index = request.session['cart'][i]
                request.session['total'] = request.session.get('total') - request.session['cart'][i]['product']['price'] * int(index['amount'])
                request.session['total_sum'] = int(request.session.get('total_sum')) - request.session['cart'][i]['product']['price'] * int(index['amount'])
                request.session['cart'].remove(index)
                
                
                request.session.modified = True
                break
                

    return redirect('shop:cart')



def clean_cart(request):
    """ 
    This function deletes all item from the CartModel 
    """
    if request.user.is_authenticated:
        obj = CartModel.objects.filter(user=request.user)
        obj.delete()
    else:    
        del request.session['cart']
        request.session.modified = True
    return redirect('shop:cart')    



def favorites(request):
    """ 
    This function returns users favorite collections from the FavoritesModel 
    """
    if request.user.is_authenticated:
        favorites = FavoritesModel.objects.filter(user=request.user)
        return render(request, 'shop/favorites.html' , {'favorites': favorites })

    return render(request, 'shop/favorites.html')
    


def add_to_favorites(request, pk):
    """ 
    This function adds a product item to the FavoritesModel 
    """
    product = ProductModel.objects.get(pk=pk)
    if request.user.is_authenticated:
        check_user_favorite = FavoritesModel.objects.filter(user=request.user, product=product)
        if check_user_favorite:
            return redirect('shop:shop')
        FavoritesModel.objects.create(user=request.user, product=product)
        return redirect('shop:favorites')

    obj = {
        "user" : None,
        "product" : product,
    }
    serializer = FavoritesSerializer(obj, many=False)
    data = serializer.data
    favorites = request.session.get('favorites', [])

    if data in favorites:
        request.session['favorites'] = favorites
        return redirect('shop:favorites')
    favorites.append(data)
    request.session['favorites'] = favorites
    return redirect('shop:favorites')



def delete_favorite_item(request, pk):
    """ 
    This function deletes an item from the FavoritesModel 
    """
    if request.user.is_authenticated:
        obj = FavoritesModel.objects.get(pk=pk)
        obj.delete()
    else:
        for i in range(len(request.session['favorites'])):
            if request.session['favorites'][i]['product']['id'] == pk:
                index = request.session['favorites'][i]
                request.session['favorites'].remove(index)
                request.session.modified = True
                break
    return redirect('shop:favorites')


def clean_favorites(request):
    """ 
    This function deletes all item from the FavoritesModel 
    """
    if request.user.is_authenticated:
        obj = FavoritesModel.objects.filter(user=request.user)
        obj.delete()
    else:    
        del request.session['favorites']
        request.session.modified = True
        # messages.success(request, 'Ваш список желаний пуст')
    return redirect('shop:favorites') 



def  change_product_amount(request, pk):
    """ 
    This function sets amount a current product when event occures on input 
    """
    if request.user.is_authenticated:
        obj = CartModel.objects.get(pk=pk)
        obj.amount = request.GET.get('cart_amount')
        obj.save()
    else:
        for i in range(len(request.session['cart'])):
            if request.session['cart'][i]['product']['id'] == pk:
                index = request.session['cart'][i]
                request.session['cart'][i]['amount'] = request.GET.get('cart_amount')
                total = []
                for j in request.session['cart']:
                    total.append(j['product']['price'] * int(j['amount']))
                
                request.session['total'] = sum(total)
                request.session['total_sum'] = DeliveryCostModel.objects.first().delivery + sum(total)
                
                request.session.modified = True
    return redirect('shop:cart')



def payment(request):
    return render(request, 'shop/payment.html')


def order_detail(request, pk):
    order = OrderModel.objects.get(pk=pk)
    carts = CartModel.objects.filter(user=order.user)
    amount = []
    for i in carts:
        amount.append(i.amount)
    return render(request, 'shop/order_detail.html', {'order':order, 'carts':carts, 'amount':sum(amount)})























    # i = 0
    # while i < len(request.session["cart"]):
    #     if request.session["cart"][i]['product']['id'] == pk:
    #         index = request.session['cart'][i]
    #         request.session['cart'].remove(index)
    #         request.session.modified = True
    #     else:
    #         i += 1
