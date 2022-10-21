from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from django.contrib.auth import password_validation, authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from phonenumber_field.validators import validate_international_phonenumber

from bank.fields import CustomRelatedField
# from bank.serializers import CustomSerializer
from .models import User, AccountTarif


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


class AccountTarifSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    monthly_price = serializers.IntegerField(required=False, min_value=0)
    transfer_limit = serializers.IntegerField(required=False, min_value=0)
    free_card_maintenance = serializers.BooleanField(required=False)
    additional_interest_rate = serializers.FloatField(required=False, min_value=0)

    def get_model(self):
        return AccountTarif


class UserSerializer(CustomSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message='Такое имя уже зарегестрировано.')
        ],
        max_length=128
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(User.objects.all(), message='Такой email уже зарегестрирован.')
        ]
    )
    phone = serializers.CharField(
        validators=[
            validate_international_phonenumber,
            UniqueValidator(User.objects.all(), message='Такой телефон уже зарегестрирован.')
        ]
    )
    password = serializers.CharField(write_only=True)
    fio = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    tarif = AccountTarifSerializer()
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='user_detail')

    def get_model(self):
        return User    

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        new_password = make_password(value)
        return new_password


class UserDepthSerializer(UserSerializer):
    tarif = serializers.PrimaryKeyRelatedField(read_only=True)


class UserCreateUpdateSerializer(UserSerializer):
    tarif = CustomRelatedField(model=AccountTarif, model_serializer=AccountTarifSerializer)
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise ValidationError('Переданы неверные данные для авторизации.')
            self.user = user

        return data
