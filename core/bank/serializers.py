import math

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
    DEFAULT_BANK_NAME
)
from .validators import number_validation
from .fields import CustomRelatedField
from .mixins import BankAccountSerializerMixin


USER_MODEL = get_user_model()


class CustomSerializer(serializers.Serializer):
    def create(self, validated_data):
        return self.get_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=validated_data.keys())
        return instance

    def get_model(self):
        raise NotImplementedError('Need to override get_model method.')


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


class BankAccountDepthSerializer(BankAccountSerializer):  # For related field in another serializers
    user = serializers.PrimaryKeyRelatedField(read_only=True)


class BankAccountUpdateSerializer(BankAccountSerializer):
    user = CustomRelatedField(model=USER_MODEL)


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

    def get_model(self):
        return Transaction


class TransactionCreateUpdateSerializer(TransactionSerializer):
    from_number = CustomRelatedField(model=BankAccount)
    to_number = CustomRelatedField(model=BankAccount)
    transaction_type = CustomRelatedField(model=TransactionType)


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

    def get_model(self):
        return Card


class CardCreateUpdateSerializer(BankAccountSerializerMixin, CardSerializer):
    card_type = CustomRelatedField(model=CardType)
    design = CustomRelatedField(model=CardDesign)
    

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
