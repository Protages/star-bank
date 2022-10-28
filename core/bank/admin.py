from django.contrib import admin
from .models import (
    BankAccount,
    Deposit,
    TransactionType,
    Transaction,
    Cashback,
    CardType,
    CardDesign,
    Card,
)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'user',)


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_number', 'to_number', 'money')


@admin.register(Cashback)
class CashbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'percent', 'get_transaction_types')

    def get_transaction_types(self, obj):
        return ', '.join(str(typ) for typ in obj.transaction_type.all())

    get_transaction_types.short_description = 'типы транзакций'


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'push_price', 'service_price',)


@admin.register(CardDesign)
class CardDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_account', 'money',)


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_account', 'money',)
