from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from phonenumber_field.validators import validate_international_phonenumber

from .models import User, AccountTarif


class AccountTarifSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    monthly_price = serializers.IntegerField(required=False)
    transfer_limit = serializers.IntegerField(required=False)
    free_card_maintenance = serializers.BooleanField(required=False)
    additional_interest_rate = serializers.FloatField(required=False)

    def create(self, validated_data):
        return AccountTarif.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=validated_data.keys())
        return instance     


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message='Такое имя уже зарегестрировано.')
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(User.objects.all(), message='Такое email уже зарегестрирован.')
        ]
    )
    phone = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message='Такое телефон уже зарегестрирован.')
        ]
    )
    password = serializers.CharField(write_only=True)
    tarif = AccountTarifSerializer(required=False)
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='user_detail')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=validated_data.keys())
        return instance        

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        new_password = make_password(value)
        return new_password

    def validate_phone(self, value):
        validate_international_phonenumber(value)
        return value

    def validate_tarif(self, value):  # Change user tarif update!
        try:
            tarif = get_object_or_404(AccountTarif, title=value['title'])  # Change user tarif update!
        except:
            raise ValidationError('Тарифа с таким id несуществует.')
        return tarif

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'request' in self.context.keys():
            host = self.context['request'].get_host()
            scheme = self.context['request'].scheme
            ret['detail'] = f'{scheme}://{host}{instance.get_absolute_url()}'
        return ret
    