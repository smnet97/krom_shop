from django.urls import path
from user.views import user_login, user_logout, UserRegistration

app_name = "user"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('sign_up/', UserRegistration.as_view(), name="sign_up")
]
