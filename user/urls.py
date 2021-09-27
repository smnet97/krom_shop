from django.urls import path
from user.views import user_login, user_logout, UserRegistration, code_confirmation, dashboard, confirm_delivery, delete_order_item


app_name = "user"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('sign_up/', UserRegistration.as_view(), name="sign_up"),
    path('code_confirmation/', code_confirmation, name="code_confirmation"),

    path('dashboard/', dashboard, name='dashboard'),
    path('confirm_delivery/<int:pk>/', confirm_delivery, name='confirm-delivery'),
    path('delete_order_item/<int:pk>/', delete_order_item, name='delete-order-item'),

    path('forgot_password/', forgot_password, name="forgot_password"),
    path('get_code/', post_code, name="post_code")

]
