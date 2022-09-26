from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, username, email, phone, password=None, **extra_fields):
        if not username:
            raise ValueError('Пользователь должен иметь логин')
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not phone:
            raise ValueError('Пользователь должен иметь номер телефона')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            **extra_fields
        )
        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, username, email, phone, password=None, **extra_fields):
        if 'is_staff' not in extra_fields:
            extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(username, email, phone, password, **extra_fields)


class AccountTarif(models.Model):
    title = models.CharField(verbose_name='Название', max_length=128)
    monthly_price = models.PositiveIntegerField(verbose_name='Месячная плата', default=0)
    transfer_limit = models.PositiveIntegerField(
        verbose_name='Лимит перевода',
        help_text='Сумма лимита перевода в месяц',
        default=50000
    )
    free_card_maintenance = models.BooleanField(
        verbose_name='Бесплатное обслуживание карт',
        default=False
    )
    additional_interest_rate = models.FloatField(
        verbose_name='Доплнительная процентная ставка',
        default=0.0
    )

    class Meta:
        verbose_name = 'Тариф Аккаунта'
        verbose_name_plural = 'Тарифы Аккаунта'

    def __str__(self):
        return f'{self.title}'


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator

    username = models.CharField(
        verbose_name='логин', max_length=128,
        unique=True,
        validators=(username_validator,)
    )
    email = models.EmailField(verbose_name='email', unique=True)
    phone = PhoneNumberField(verbose_name='номер телефона', unique=True)
    password = models.CharField(verbose_name='пароль', max_length=128)

    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)
    is_staff = models.BooleanField(verbose_name='Персонал', default=False)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    fio = models.CharField(verbose_name='ФИО', max_length=128, blank=True)
    country = models.CharField(verbose_name='Страна', max_length=128, blank=True)
    tarif = models.ForeignKey(
        AccountTarif,
        verbose_name='Тариф',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(verbose_name='Время регистрации', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Последний вход', blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def __str__(self):
        if self.fio:
            return f'{self.fio}'
        return f'{self.username}'
