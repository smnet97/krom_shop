from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST

from .models import UserModel
from .forms import LoginForm, RegistrationForm, GetCodeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from krom.helpers import send_sms_code, validate_sms_code
from django.contrib.auth.hashers import make_password


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
                # user = UserModel(**data)
                # user.set_password(user.password)
                # print('*************')
                # print(user.username)
                # user.save()
                messages.success(request, "Вы успешно зарегистрировались.")
                phone = data['username']
                send_sms_code(request, phone)
                request.session["recovery"] = {
                    "phone": phone,
                    "password": data['password']
                }
                get_code_form = GetCodeForm()
                return render(request, "users/confirmation.html", {
                    "form": get_code_form,
                    "request.title": "Отправить код"
                })
            else:
                form.add_error('username', "Этот номер телефона зарегистрирован!")
                return render(request, 'users/sign_up.html', {
                    'form': form,
                })

        return render(request, "users/sign_up.html", {
            'form': form
        })


@require_POST
def code_confirmation(request):
    request.title = "Код подтверждения"

    data = request.session["recovery"]
    print(data)
    if request.method != "POST" or data['phone'] is None:
        return redirect("user:sign_up")

    code = request.POST.get("code")
    print(code)
    #
    if data['phone'] is None:  #or not validate_sms_code(data["phone"], code)
        return False
    print(data)
    user = UserModel.objects.create(username=data["phone"], password=make_password(data["password"]))
    # user.set_password(data["password"])
    # print(user)
    # user.save()
    if user is not None:
        login(request, user)
        return redirect("shop:home")

    return redirect("user:sign_up")
