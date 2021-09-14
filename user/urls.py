from django.urls import path
from user.views import user_login, user_logout, UserRegistration, code_confirmation

app_name = "user"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('sign_up/', UserRegistration.as_view(), name="sign_up"),
    path('code_confirmation/', code_confirmation, name="code_confirmation")
]
