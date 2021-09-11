from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')


def detail(request):
    return render(request, 'shop/detail.html')
