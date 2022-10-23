from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core import exceptions

from .validators import number_validation


USER_MODEL = get_user_model()
DEFAULT_BANK_NAME = 'Star-Bank'
ALLOWED_CURRENCY = [
    ('RUB', 'Рубль'),
    ('USD', 'Доллар'),
    ('EUR', 'Евро')
]


def get_completion_data():
    now = date.today()
    completion_year = 3
    completion_date = date(
        year=now.year + completion_year,
        month=now.month,
        day=now.day
    )
    return completion_date


class BankAccount(models.Model):
    number = models.CharField(
        verbose_name='номер счета',
        validators=(number_validation, ),
        max_length=20,
        unique=True,
    )
    user = models.ForeignKey(
        USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE
    )
    bank_name = models.CharField(
        verbose_name='банк', max_length=128, default=DEFAULT_BANK_NAME
    )

    class Meta:
        verbose_name = 'счет'
        verbose_name_plural = 'счета'

    def __str__(self):
        return f'{self.number} - {self.user}'

    def get_related_card_or_deposit(self):
        related_obj = getattr(self, 'card', getattr(self, 'deposit', None))
        if related_obj is None:
            raise exceptions.ObjectDoesNotExist(
                f'У объекта BankAccount {self.pk} нет связанного Card или Deposit.'
            )
        return related_obj


class TransactionType(models.Model):
    title = models.CharField(verbose_name='название', max_length=128)

    class Meta:
        verbose_name = 'тип транзакции'
        verbose_name_plural = 'типы транзакций'

    def __str__(self):
        return f'{self.title}'


class Transaction(models.Model):
    from_number = models.ForeignKey(
        BankAccount,
        verbose_name='от счета',
        related_name='transaction_from',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    to_number = models.ForeignKey(
        BankAccount,
        verbose_name='к счета',
        related_name='transaction_to',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    money = models.FloatField(verbose_name='сумма')
    currency = currency = models.CharField(
        verbose_name='валюта',
        max_length=64,
        choices=ALLOWED_CURRENCY,
        default='RUB'
    )
    date = models.DateTimeField(verbose_name='дата', auto_now_add=timezone.now())
    transaction_type = models.ForeignKey(
        TransactionType,
        verbose_name='тип',
        on_delete=models.CASCADE
    )
    cashback_money = models.IntegerField(verbose_name='Сумма кэшбэка', blank=True, default=0)

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'

    def __str__(self):
        return f'{self.pk} - {self.money}{self.currency}'


class Cashback(models.Model):
    title = models.CharField(verbose_name='название', max_length=128)
    percent = models.PositiveIntegerField(verbose_name='процент', default=0)
    transaction_type = models.ManyToManyField(
        TransactionType,
        verbose_name='типы транзакций'
    )

    class Meta:
        verbose_name = 'кэшбэк'
        verbose_name_plural = 'кэшбэки'

    def __str__(self):
        return f'{self.title}'


class CardType(models.Model):
    title = models.CharField(verbose_name='название', max_length=128)
    push_price = models.PositiveIntegerField(
        verbose_name='цена уведомлений', default=30
    )
    service_price = models.PositiveIntegerField(
        verbose_name='цена обсуживания', default=50
    )
    cashbacks = models.ManyToManyField(Cashback, verbose_name='кэшбэк')

    class Meta:
        verbose_name = 'тип карт'
        verbose_name_plural = 'типы карт'

    def __str__(self):
        return f'{self.title}'


class CardDesign(models.Model):
    title = models.CharField(verbose_name='название', max_length=128)
    author = models.CharField(
        verbose_name='автор',
        max_length=128,
        blank=True, null=True
    )
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    example = models.CharField(
        verbose_name='пример',
        max_length=128,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'дизайн карт'
        verbose_name_plural = 'дизайны карт'

    def __str__(self):
        return f'{self.title}'


class Card(models.Model):
    bank_account = models.OneToOneField(
        BankAccount,
        verbose_name='счет',
        on_delete=models.CASCADE
    )
    currency = models.CharField(
        verbose_name='валюта',
        max_length=64,
        choices=ALLOWED_CURRENCY,
        default='RUB'
    )
    money = models.FloatField(verbose_name='сумма', default=0.0)
    card_type = models.ForeignKey(
        CardType,
        verbose_name='тип карты',
        on_delete=models.CASCADE
    )
    is_push = models.BooleanField(verbose_name='уведомления', default=False)
    date_issue = models.DateField(
        verbose_name='дата создания',
        default=date.today
    )
    completion_date = models.DateField(
        verbose_name='дата истечения',
        default=get_completion_data
    )
    design = models.ForeignKey(
        CardDesign,
        verbose_name='дизайн',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    cashback_money = models.IntegerField(verbose_name='сумма кэшбэка', blank=True, default=0)
    is_blocked = models.BooleanField(verbose_name='заблокирована', blank=True, default=False)   
    
    class Meta:
        verbose_name = 'карта'
        verbose_name_plural = 'карты'

    def __str__(self):
        return f'{self.bank_account} - {self.money}{self.currency}'


class Deposit(models.Model):
    bank_account = models.OneToOneField(
        BankAccount,
        verbose_name='счет',
        on_delete=models.CASCADE
    )
    currency = models.CharField(
        verbose_name='валюта', max_length=64, choices=ALLOWED_CURRENCY, default='RUB'
    )
    money = models.FloatField(verbose_name='сумма', default=0.0)
    interest_rate = models.FloatField(verbose_name='ставка %', default=0.0)
    min_value = models.PositiveIntegerField(verbose_name='минимальная сумма', default=0)
    max_value = models.PositiveIntegerField(
        verbose_name='максимальная сумма', default=100000
    )
    date_issue = models.DateField(
        verbose_name='дата создания', 
        default=date.today
    )
    completion_date = models.DateField(
        verbose_name='дата истечения',
        default=get_completion_data
    )
    
    class Meta:
        verbose_name = 'вклад'
        verbose_name_plural = 'вклады'

    def __str__(self):
        return f'{self.bank_account} - {self.money}{self.currency}'
