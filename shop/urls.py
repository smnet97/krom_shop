from django.urls import path
from .views import home

app_name = 'shop'

urlpatterns = [
    path('', home, name='home')
]