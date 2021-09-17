from django.core.exceptions import ValidationError

from user.models import UserModel


class PhoneValidatorTest:
    requires_context = False

    def __call__(self, value):
        if not UserModel.objects.filter(username=value).exists():
            raise ValidationError("Этот номер телефона не существует!")