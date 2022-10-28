from rest_framework import serializers


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
