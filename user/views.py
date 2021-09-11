from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .models import UserModel
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from krom.helpers import send_sms_code


def user_login(request):
    request.title = "Авторизоваться"

    form = LoginForm()

    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Добро пожаловать !!!  {}".format(user.username))
                return redirect('shop:home')

            form.add_error('password', "Номер телефона или пароль неверны !")
            return render(request, 'users/login.html', {
                'form': form,
            })
    return render(request, 'users/login.html', {
        'form': form
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect("user:login")


class UserRegistration(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = "Регистрация"

    def get(self, request):
        form = RegistrationForm()
        return render(request, "users/sign_up.html", {
            'form': form
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid() and request.method == "POST":
            data = form.cleaned_data
            del data['confirm']
            if not UserModel.objects.filter(username=data['username']).exists():
                user = UserModel(**data)
                user.set_password(user.password)
                # print('*************')
                # print(user.username)
                user.save()
                messages.success(request, "Вы успешно зарегистрировались.")
                send_sms_code(request, data['username'])
                return redirect('user:login')
            else:
                form.add_error('username', "Этот номер телефона зарегистрирован!")
                return render(request, 'users/sign_up.html', {
                    'form': form,
                })

        return render(request, "users/sign_up.html", {
            'form': form
        })





