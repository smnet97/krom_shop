from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    request.title = "Авторизоваться"

    form = LoginForm()

    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(phone=form.cleaned_data["phone"], password=form.cleaned_data['password'])
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




