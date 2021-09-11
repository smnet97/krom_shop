from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from krom.validators import PhoneValidator


class UserManager(BaseUserManager):

    def __create_user(self, phone, password, **kwargs):
        phone = PhoneValidator.clean(phone)
        validator = PhoneValidator()
        validator(phone)

        user = UserModel(**kwargs)
        user.phone = phone
        user.set_password(password)
        user.save()

    def create_user(self, *args, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_staff') or kwargs.get('is_superuser'):
            raise Exception("User is_staff=False va is_superuser=False bo'lishi shart!")

        return self.__create_user(*args, **kwargs)

    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff') or not kwargs.get('is_superuser'):
            raise Exception("User is_staff=True va is_superuser=True bo'lishi shart!")

        return self.__create_user(*args, **kwargs)


class UserModel(AbstractUser):
    objects = UserManager()
    password = models.CharField(max_length=100, help_text="Пожалуйста, укажите свой пароль")
    username = models.CharField(max_length=15, unique=True,
                             validators=[PhoneValidator()], help_text="Пожалуйста, укажите свой пароль")

    # USERNAME_FIELD = "phone"
    username_validator = PhoneValidator()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.phone


class SmsCode(models.Model):
    phone = models.CharField(max_length=16, db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    code = models.CharField(max_length=10)
    expire_at = models.DateTimeField(db_index=True)

    class Meta:
        index_together = []


class SmsAttempt(models.Model):
    phone = models.CharField(max_length=16, db_index=True)
    counter = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(db_index=True)
