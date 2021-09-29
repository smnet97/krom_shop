from django.urls import path
from .views import check_apelsin

app_name = 'apelsinuz'

urlpatterns = [
    path('', check_apelsin, name='check-apelsin'),
]