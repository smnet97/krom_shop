from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from user.models import UserModel
from krom.validators import PhoneValidator
from krom.validators2 import PhoneValidatorTest


class LoginForm(forms.Form):
    username = forms.CharField(max_length=14, required=True,
                               widget=forms.TextInput(attrs={'placeholder': '998971234567'}), label=False)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                               validators=[MinLengthValidator(6)], label=False)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=14, required=True, validators=[PhoneValidator()],
                               widget=forms.TextInput(attrs={'placeholder': '998971234567'}), label=False)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                               validators=[MinLengthValidator(6)], label=False)
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                              validators=[MinLengthValidator(6)], label=False)

    def clean_phone(self):
        if UserModel.objects.filter(phone=self.cleaned_data.get("phone")).exists():
            raise ValidationError("Этот номер телефона зарегистрирован")

        return self.cleaned_data['phone']

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise ValidationError('Пароли не совпадают!')

        return self.cleaned_data['confirm']


class ForgotPassword(forms.Form):
    username = forms.CharField(max_length=16, label=False,
                               widget=forms.TextInput(attrs=({'placeholder': '998971234567',
                                                              'id': 'phone_number'})),
                               validators=[PhoneValidator(), PhoneValidatorTest()], required=True)
    new_password = forms.CharField(max_length=18, widget=forms.PasswordInput(attrs=({'id': 'new_password'})),
                                   required=True, validators=[MinLengthValidator(6)], label=False)
    confirm_password = forms.CharField(max_length=18, widget=forms.PasswordInput(attrs=({'id': 'confirm_password'})),
                                       required=True, validators=[MinLengthValidator(6)], label=False)

    def clean_confirm(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise ValidationError("Пароли не совпадают!")

        return self.cleaned_data['confirm_password']


class GetCodeForm(forms.Form):
    code = forms.IntegerField(max_value=6, label=False,
                              widget=forms.TextInput(attrs=({"class": "rounded-15", 'placeholder': 'Введите код',
                                                             'id': "code"})), required=True)
