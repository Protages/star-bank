from typing import Iterable
from rest_framework import serializers
from rest_framework.validators import ValidationError


class CustomRelatedField(serializers.RelatedField):
    """
    Кастомное поле, призванное избежать чрезмерного кол-ва запросов в бд.
    В качестве входных значений принимает число.
    Необходимо передать model и modle_serializer.
    Поиск осуществляется по полю lookup_field='pk'.
    Если передается many=True, необходимо будет передать model_serializer.
    Встроенная валидации на существование объекта в бд.
    """

    def __new__(cls, *args, **kwargs):
        if kwargs.pop('many', False):
            return CustomManyRelatedField(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, model, model_serializer, lookup_field='pk', **kwargs):
        self.model = model
        self.model_serializer = model_serializer
        self.lookup_field = lookup_field
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.model_serializer().to_representation(value)

    def to_internal_value(self, data):
        try:
            lookup_kwargs = {self.lookup_field: data}
            obj = self.model.objects.get(**lookup_kwargs)
        except:
            raise ValidationError(
                f'Объекта с {self.lookup_field} = {data} не существует.'
            )
        return obj

    def get_queryset(self):
        pass


class CustomManyRelatedField(CustomRelatedField):
    def to_internal_value(self, data):
        if not isinstance(data, Iterable):
            raise ValidationError('Необходимо передать список.')
        try:
            related_obj_list = []
            for pk_value in list(data):
                pk_v = pk_value
                lookup_kwargs = {self.lookup_field: pk_value}
                related_obj_list.append(self.model.objects.get(**lookup_kwargs))
        except:
            raise ValidationError(
                f'Объекта с {self.lookup_field} = {pk_v} не существует.'
            )
        return related_obj_list

    def to_representation(self, manager):
        # manager - ManyRelatedManager (django.db.models.fields.related_descriptors)
        queryset = manager.get_queryset()
        return self.model_serializer(many=True).to_representation(queryset)
