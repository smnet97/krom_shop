from django.urls import path

app_name = "user_app"

urlpatterns = [
    path('', user_login, name='login')
]
