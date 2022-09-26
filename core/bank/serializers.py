from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueValidator

from .models import (
    BankAccount,
    TransactionType,
    Transaction,
    Cashback,
    CardType,
    CardDesign,
    Card,
    Deposit,
    ALLOWED_CURRENCY
)
from .validators import number_validation
from .fields import CustomRelatedField


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
    user = serializers.PrimaryKeyRelatedField(queryset=USER_MODEL.objects.all())
    bank_name = serializers.CharField(required=False)

    def get_model(self):
        return BankAccount


class BankAccountDepthSerializer(BankAccountSerializer):  # For related field in another serializers
    user = serializers.PrimaryKeyRelatedField(read_only=True)


class TransactionTypeSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    def get_model(self):
        return TransactionType


class TransactionSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    from_number = BankAccountDepthSerializer()
    to_number = BankAccountDepthSerializer()
    money = serializers.FloatField()
    currency = serializers.ChoiceField(choices=ALLOWED_CURRENCY)
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
    title = serializers.CharField()
    percent = serializers.IntegerField()
    transaction_type = TransactionTypeSerializer(many=True)

    def get_model(self):
        return Cashback


class CashbackCreateUpdateSerializer(CashbackSerializer):
    transaction_type = CustomRelatedField(
        model=TransactionType, 
        many=True, 
        model_serializer=TransactionTypeSerializer,
        required=False
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
