from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.serializers import UserDepthSerializer
from .models import BankAccount, DEFAULT_BANK_NAME
from .fields import CustomRelatedField
from .validators import number_validation


USER_MODEL = get_user_model()


class BankAccountSerializerMixin(serializers.Serializer):
    """
    Миксин для сериализаторов Card и Deposit.
    Добавляет поля number, user, bank_name - для создания BankAccount.
    Переопределяет методы create() и update(),
    которые создают и обновляют сразу дву записи -
    Card или Deposit и связанный BankAccount.
    """

    number = serializers.CharField(
        validators=[
            number_validation,
            UniqueValidator(
                BankAccount.objects.all(), message='Поле number должно быть уникальным.'
            )
        ],
        write_only=True
    )
    user = CustomRelatedField(
        model=USER_MODEL, model_serializer=UserDepthSerializer, write_only=True
    )
    bank_name = serializers.CharField(
        default=DEFAULT_BANK_NAME,
        max_length=128,
        required=False,
        write_only=True
    )

    @property
    def bank_account_fields(self):
        return ('number', 'user', 'bank_name')

    def create(self, validated_data):
        bank_account_validated_data = {
            field: validated_data.pop(field)
            for field in self.bank_account_fields
            if field in validated_data
        }

        with transaction.atomic():
            bank_account = BankAccount.objects.create(**bank_account_validated_data)
            obj = self.get_model()(**validated_data)
            obj.bank_account = bank_account
            obj.save()

        return obj

    def update(self, instance, validated_data):
        bank_account = instance.bank_account
        bank_account_validated_data = {
            field: validated_data.pop(field)
            for field in self.bank_account_fields
            if field in validated_data
        }

        with transaction.atomic():
            for key, value in bank_account_validated_data.items():
                setattr(bank_account, key, value)
            bank_account.save(update_fields=bank_account_validated_data.keys())

            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save(update_fields=validated_data.keys())

        return instance
