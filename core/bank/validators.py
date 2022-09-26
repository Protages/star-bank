import re
from rest_framework.validators import ValidationError


NUMBER_REGEX = r'([0-9]){20}'


def number_validation(value):
    if re.fullmatch(NUMBER_REGEX, str(value)) is None:
        raise ValidationError(f'number должен быть равен 20 символам и состоять из чисел.')
