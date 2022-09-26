from rest_framework import serializers
from rest_framework.validators import ValidationError


class CustomRelatedField(serializers.RelatedField):
    """ Кастомное поле, призванное избежать чрезмерного кол-ва запросов в бд.
    В качестве входных значений принимает числа и 'число'.
    Необходимо передать model=..., поиск осуществляется по полю 'pk'.
    Если передается many=True, необходимо передать model_serializer.
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
        return value.pk

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
        print('in to_internal_value' ,data)
        try:
            obj_list = []
            for pk_value in list(data):
                pk_v = pk_value
                lookup_kwargs = {self.lookup_field: pk_value}
                print(lookup_kwargs)
                obj_list.append(self.model.objects.get(**lookup_kwargs))
        except:
            raise ValidationError(f'Объекта с {self.lookup_field} = {pk_v} не существует.')
        return obj_list

    def to_representation(self, value):
        obj_list = getattr(self.parent.context['view'].get_object(), self.field_name).all()
        assert not self.model_serializer is None, 'Необходимо передать model_serializer, если many=True.' 
        
        # if self.parent.context['request'].method == 'PUT':
        #     return [obj.id for obj in obj_list]
        return self.model_serializer(many=True).to_representation(obj_list)
