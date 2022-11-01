from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueValidator

from user.serializers import UserDepthSerializer
from .models import (
    BankAccount,
    TransactionType,
    Transaction,
    Cashback,
    CardType,
    CardDesign,
    Card,
    Deposit,
    ALLOWED_CURRENCY,
)
from .validators import number_validation
from .custom_serializer import CustomSerializer
from .fields import CustomRelatedField
from .mixins import BankAccountSerializerMixin


USER_MODEL = get_user_model()


class BankAccountSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    number = serializers.CharField(
        validators=[
            number_validation,
            UniqueValidator(
                BankAccount.objects.all(), message='Поле number должно быть уникальным.'
            )
        ]
    )
    user = UserDepthSerializer()
    bank_name = serializers.CharField(max_length=128, required=False)

    def get_model(self):
        return BankAccount


# For related field in another serializers
class BankAccountDepthSerializer(BankAccountSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)


class BankAccountCreateUpdateSerializer(BankAccountSerializer):
    user = CustomRelatedField(model=USER_MODEL, model_serializer=UserDepthSerializer)


class TransactionTypeSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)

    def get_model(self):
        return TransactionType


class TransactionSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    from_number = BankAccountDepthSerializer()
    to_number = BankAccountDepthSerializer()
    money = serializers.FloatField(min_value=0.1)
    currency = serializers.ChoiceField(required=False, choices=ALLOWED_CURRENCY)
    date = serializers.DateTimeField(read_only=True)
    transaction_type = TransactionTypeSerializer()
    cashback_money = serializers.IntegerField(read_only=True)

    def get_model(self):
        return Transaction


class TransactionCreateUpdateSerializer(TransactionSerializer):
    from_number = CustomRelatedField(
        model=BankAccount, model_serializer=BankAccountDepthSerializer
    )
    to_number = CustomRelatedField(
        model=BankAccount, model_serializer=BankAccountDepthSerializer
    )
    transaction_type = CustomRelatedField(
        model=TransactionType,
        model_serializer=TransactionTypeSerializer
    )

    def validate(self, data):
        self.transaction_errors = {}
        from_number = data.get('from_number')
        to_number = data.get('to_number')

        if from_number == to_number:
            raise ValidationError('Счета from_number и to_number должны быть разными.')

        currency = data.get('currency', 'RUB')
        money = data.get('money')

        self.valid_enough_money(from_number, money)
        self.valid_correct_currency(from_number, to_number, currency)

        if len(self.transaction_errors) != 0:
            raise ValidationError(self.transaction_errors)

        return data

    def valid_enough_money(self, from_number, money):
        from_obj = from_number.get_related_card_or_deposit()

        if not from_obj.money >= money:
            obj_type = 'карты' if isinstance(from_obj, Card) else 'депозита'
            if 'from_number' not in self.transaction_errors.keys():
                self.transaction_errors['from_number'] = []

            self.transaction_errors['from_number'].append(
                f'У {obj_type} {from_number.number} недостаточно средств.'
            )

    def valid_correct_currency(self, from_number, to_number, currency):
        from_obj = from_number.get_related_card_or_deposit()
        to_obj = to_number.get_related_card_or_deposit()

        if from_obj.currency != currency:
            obj_type = 'карты' if isinstance(from_obj, Card) else 'депозита'
            if 'from_number' not in self.transaction_errors.keys():
                self.transaction_errors['from_number'] = []

            self.transaction_errors['from_number'].append(
                f'У {obj_type} {from_number.number} валюта - {from_obj.currency}, '
                f'у транзакции - {currency}'
            )

        if to_obj.currency != currency:
            obj_type = 'карты' if isinstance(to_obj, Card) else 'депозита'
            if 'to_number' not in self.transaction_errors.keys():
                self.transaction_errors['to_number'] = []

            self.transaction_errors['to_number'].append(
                f'У {obj_type} {to_number.number} валюта - {to_obj.currency}, '
                f'у транзакции - {currency}'
            )

    def create(self, validated_data):
        from_number = validated_data.get('from_number')
        to_number = validated_data.get('to_number')
        transaction_type = validated_data.get('transaction_type')
        money = validated_data.get('money')

        cashback_money = self.calculate_cashback_money(
            from_number, transaction_type, money
        )

        with transaction.atomic():
            from_obj = from_number.get_related_card_or_deposit()
            to_obj = to_number.get_related_card_or_deposit()
            from_obj.money -= money
            to_obj.money += money

            if cashback_money != 0:
                from_obj.cashback_money += cashback_money
                validated_data['cashback_money'] = cashback_money

            from_obj.save()
            to_obj.save()

        return Transaction.objects.create(**validated_data)

    def calculate_cashback_money(self, from_number, transaction_type, money):
        from_obj = from_number.get_related_card_or_deposit()

        if not isinstance(from_obj, Card):
            return 0

        card_type = from_obj.card_type
        cashbacks = card_type.cashbacks.all()
        percent = 0

        for cashback in cashbacks:
            transaction_types = cashback.transaction_type.all()
            if transaction_type in transaction_types:
                percent = cashback.percent if cashback.percent > percent else percent

        return int(money * (percent / 100))


class CashbackSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    percent = serializers.IntegerField(min_value=0, max_value=100)
    transaction_type = TransactionTypeSerializer(many=True)

    def get_model(self):
        return Cashback


class CashbackDepthSerializer(CashbackSerializer):
    transaction_type = serializers.PrimaryKeyRelatedField(read_only=True, many=True)


class CashbackCreateUpdateSerializer(CashbackSerializer):
    transaction_type = CustomRelatedField(
        model=TransactionType,
        many=True,
        model_serializer=TransactionTypeSerializer
    )

    def create(self, validated_data):
        transaction_types = validated_data.pop('transaction_type')
        obj = Cashback.objects.create(**validated_data)
        obj.transaction_type.set(transaction_types)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        transaction_types = validated_data.pop('transaction_type', None)
        if transaction_types is not None:
            instance.transaction_type.set(transaction_types)
        return super().update(instance, validated_data)


class CardTypeSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    push_price = serializers.IntegerField(min_value=0)
    service_price = serializers.IntegerField(min_value=0)
    cashbacks = CashbackDepthSerializer(many=True)

    def get_model(self):
        return CardType


class CardTypeDepthSerializer(CardTypeSerializer):
    cashbacks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class CardTypeCreateUpdateSerializer(CardTypeSerializer):
    cashbacks = CustomRelatedField(
        model=Cashback,
        many=True,
        model_serializer=CashbackDepthSerializer
    )

    def create(self, validated_data):
        cashbacks = validated_data.pop('cashbacks')
        obj = CardType.objects.create(**validated_data)
        obj.cashbacks.set(cashbacks)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        cashbacks = validated_data.pop('cashbacks', None)
        if cashbacks is not None:
            instance.cashbacks.set(cashbacks)
        return super().update(instance, validated_data)


class CardDesignSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    author = serializers.CharField(max_length=128, required=False)
    description = serializers.CharField(required=False)
    example = serializers.CharField(max_length=128, required=False)

    def get_model(self):
        return CardDesign


class CardSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    bank_account = BankAccountDepthSerializer(read_only=True)
    currency = serializers.ChoiceField(choices=ALLOWED_CURRENCY)
    money = serializers.FloatField()
    card_type = CardTypeDepthSerializer()
    is_push = serializers.BooleanField(required=False)
    date_issue = serializers.DateField(read_only=True)
    completion_date = serializers.DateField(read_only=True)
    design = CardDesignSerializer()
    cashback_money = serializers.IntegerField(read_only=True)
    is_blocked = serializers.BooleanField(required=False)

    def get_model(self):
        return Card


class CardCreateUpdateSerializer(BankAccountSerializerMixin, CardSerializer):
    card_type = CustomRelatedField(
        model=CardType, model_serializer=CardTypeDepthSerializer
    )
    design = CustomRelatedField(model=CardDesign, model_serializer=CardDesignSerializer)


class DepositSeializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    bank_account = BankAccountDepthSerializer(read_only=True)
    currency = serializers.ChoiceField(choices=ALLOWED_CURRENCY)
    money = serializers.FloatField()
    interest_rate = serializers.FloatField(required=False, min_value=0.0)
    min_value = serializers.IntegerField(required=False, min_value=0)
    max_value = serializers.IntegerField(required=False, min_value=0)
    date_issue = serializers.DateField(read_only=True)
    completion_date = serializers.DateField(read_only=True)

    def get_model(self):
        return Deposit


class DepositCreateUpdateSerializer(BankAccountSerializerMixin, DepositSeializer):
    pass
