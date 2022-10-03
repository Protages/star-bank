from rest_framework import serializers
from rest_framework.validators import ValidationError
# from django.db.models.fields.related_descriptors


class CustomRelatedField(serializers.RelatedField):
    """ Кастомное поле, призванное избежать чрезмерного кол-ва запросов в бд.
    В качестве входных значений принимает число.
    Необходимо передать model=..., поиск осуществляется по полю lookup_field='pk'.
    Если передается many=True, необходимо будет передать model_serializer.
    Встроенная валидации на существование объекта в бд. """
    
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('many', False):
            return CustomManyRelatedField(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, model, lookup_field='pk', model_serializer=None, **kwargs):
        self.model = model
        self.lookup_field = lookup_field
        self.model_serializer = model_serializer
        super().__init__(**kwargs)

    def to_representation(self, value):
        return getattr(value, self.lookup_field)

    def to_internal_value(self, data):
        try:
            lookup_kwargs = {self.lookup_field: data}
            obj = self.model.objects.get(**lookup_kwargs)
        except:
            raise ValidationError(f'Объекта с {self.lookup_field} = {data} не существует.')
        return obj

    def get_queryset(self): pass


class CustomManyRelatedField(CustomRelatedField):
    def to_internal_value(self, data):
        try:
            related_obj_list = []
            for pk_value in list(data):
                pk_v = pk_value
                lookup_kwargs = {self.lookup_field: pk_value}
                related_obj_list.append(self.model.objects.get(**lookup_kwargs))
        except:
            raise ValidationError(f'Объекта с {self.lookup_field} = {pk_v} не существует.')
        return related_obj_list

    def to_representation(self, manager):  # manager - ManyRelatedManager (django.db.models.fields.related_descriptors)
        queryset = manager.get_queryset()
        return self.model_serializer(many=True).to_representation(queryset)
